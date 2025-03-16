from typing import Dict, Any, Callable
import hashlib
import time

class SmartContract:
    def __init__(self, code: str, initial_state: Dict[str, Any] = None):
        self.code = code
        self.state = initial_state or {}
        self.contract_address = self._generate_address()
        self.functions: Dict[str, Callable] = {}
        
    def _generate_address(self) -> str:
        """Generate unique contract address"""
        contract_string = f"{self.code}{time.time()}"
        return "CONTRACT-" + hashlib.sha256(contract_string.encode()).hexdigest()[:32]
        
    def register_function(self, name: str, func: Callable) -> None:
        """Register a contract function"""
        self.functions[name] = func
        
    def execute(self, function_name: str, *args, **kwargs) -> Any:
        """Execute a contract function"""
        if function_name not in self.functions:
            raise ValueError(f"Function {function_name} not found in contract")
        return self.functions[function_name](*args, **kwargs)

class TokenContract(SmartContract):
    def __init__(self, initial_supply: float):
        super().__init__("TokenContract", {"total_supply": initial_supply, "balances": {}})
        self.register_function("transfer", self.transfer)
        self.register_function("balance_of", self.balance_of)
        
    def transfer(self, from_address: str, to_address: str, amount: float) -> bool:
        """Transfer tokens between addresses"""
        balances = self.state["balances"]
        if balances.get(from_address, 0) < amount:
            return False
        
        balances[from_address] = balances.get(from_address, 0) - amount
        balances[to_address] = balances.get(to_address, 0) + amount
        return True
        
    def balance_of(self, address: str) -> float:
        """Get token balance of address"""
        return self.state["balances"].get(address, 0) 