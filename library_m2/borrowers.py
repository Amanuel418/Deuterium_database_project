import sqlite3
import re
from config import DB_PATH

def generate_card_id():
    """
    Generate a new card ID in the format ID###### (e.g., ID000001).
    Finds the highest existing card ID and increments it.
    
    Returns:
        str: New card ID
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Get all existing card IDs that match the pattern ID######
    cur.execute("SELECT Card_id FROM BORROWER WHERE Card_id LIKE 'ID%' ORDER BY Card_id DESC LIMIT 1")
    result = cur.fetchone()
    
    conn.close()
    
    if result:
        # Extract the numeric part
        match = re.search(r'ID(\d+)', result[0])
        if match:
            num = int(match.group(1))
            new_num = num + 1
            return f"ID{new_num:06d}"
    
    # If no existing IDs found, start with ID000001
    return "ID000001"


def create_borrower(bname, address, phone, ssn):
    """
    Create a new borrower in the system.
    
    Args:
        bname (str): Borrower name (required)
        address (str): Borrower address (required)
        phone (str): Borrower phone number (required)
        ssn (str): Social Security Number (required, must be unique)
    
    Returns:
        tuple: (success: bool, message: str, card_id: str or None)
    """
    # Validate required fields
    if not bname or not bname.strip():
        return False, "Error: Borrower name is required.", None
    
    if not address or not address.strip():
        return False, "Error: Address is required.", None
    
    if not phone or not phone.strip():
        return False, "Error: Phone number is required.", None
    
    if not ssn or not ssn.strip():
        return False, "Error: SSN is required.", None
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    try:
        # Check if SSN already exists
        cur.execute("SELECT * FROM BORROWER WHERE Ssn = ?", (ssn,))
        existing_borrower = cur.fetchone()
        
        if existing_borrower:
            conn.close()
            return False, f"Error: A borrower with SSN '{ssn}' already exists. Each borrower is allowed exactly one library card.", None
        
        # Generate new card ID
        card_id = generate_card_id()
        
        # Insert new borrower
        cur.execute("""
            INSERT INTO BORROWER (Card_id, Bname, Address, Phone, Ssn)
            VALUES (?, ?, ?, ?, ?)
        """, (card_id, bname.strip(), address.strip(), phone.strip(), ssn.strip()))
        
        conn.commit()
        conn.close()
        
        return True, f"Successfully created new borrower. Card ID: {card_id}", card_id
    
    except sqlite3.IntegrityError as e:
        conn.close()
        if "UNIQUE constraint" in str(e):
            return False, f"Error: A borrower with SSN '{ssn}' already exists. Each borrower is allowed exactly one library card.", None
        return False, f"Database integrity error: {str(e)}", None
    
    except sqlite3.Error as e:
        conn.close()
        return False, f"Database error: {str(e)}", None


def get_borrower(card_id):
    """
    Get borrower information by card ID.
    
    Args:
        card_id (str): Borrower card ID
    
    Returns:
        dict or None: Borrower information or None if not found
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM BORROWER WHERE Card_id = ?", (card_id,))
    result = cur.fetchone()
    
    conn.close()
    
    if result:
        return {
            'Card_id': result['Card_id'],
            'Bname': result['Bname'],
            'Address': result['Address'],
            'Phone': result['Phone'],
            'Ssn': result['Ssn']
        }
    
    return None


def search_borrowers(search_term):
    """
    Search for borrowers by name, card ID, or SSN (case-insensitive substring matching).
    
    Args:
        search_term (str): Search query
    
    Returns:
        list: List of borrower dictionaries
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    search_pattern = f"%{search_term.lower()}%"
    
    query = """
    SELECT * FROM BORROWER
    WHERE LOWER(Card_id) LIKE ?
       OR LOWER(Bname) LIKE ?
       OR LOWER(Ssn) LIKE ?
    ORDER BY Card_id
    """
    
    cur.execute(query, (search_pattern, search_pattern, search_pattern))
    results = cur.fetchall()
    
    borrowers = []
    for row in results:
        borrowers.append({
            'Card_id': row['Card_id'],
            'Bname': row['Bname'],
            'Address': row['Address'],
            'Phone': row['Phone'],
            'Ssn': row['Ssn']
        })
    
    conn.close()
    return borrowers


if __name__ == "__main__":
    # Test create_borrower
    success, message, card_id = create_borrower(
        "John Doe",
        "123 Main St, City, State",
        "(555) 123-4567",
        "123-45-6789"
    )
    print(message)
    if success:
        print(f"Card ID: {card_id}")

