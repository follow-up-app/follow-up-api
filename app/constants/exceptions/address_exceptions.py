class AddressNotFoundError(Exception):
    MESSAGE = "Address not found"

class AddressNotRegisterError(Exception):
    MESSAGE = "O cliente não possui nenhum endereço cadastado. Faça o cadastro de um endereço em cadastro > cliente > endereço"