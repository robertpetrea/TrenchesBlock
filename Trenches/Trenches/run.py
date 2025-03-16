from api import app
from database import BlockchainDB
from logger import BlockchainLogger
import os
from dotenv import load_dotenv

def initialize_blockchain():
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    db = BlockchainDB()
    logger = BlockchainLogger()
    
    # Log startup
    logger.logger.info("Blockchain starting up...")
    
    # Run the application
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    initialize_blockchain() 