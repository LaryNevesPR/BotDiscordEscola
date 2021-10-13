from JasonManager import Ler_Empregos, Guardar_Empregos

EmpregosDic = Ler_Empregos()

comando = 'continue'
while comando != "sair":
    comando = input("Digite o comando: (n, sair)")
    if comando.strip() == "n":
        EmpregoNome = input('Nome do Emprego= ').strip()
        DinheiroMin =input('Dinheiro Minimo= ').strip()
        DinheiroMax = input('Dinheiro Maximo= ').strip()
        EmpregosDic[EmpregoNome] = {
        "nomeemprego": EmpregoNome,
        "dinheiromin": DinheiroMin,
        "dinheiromax": DinheiroMax
        }
        Guardar_Empregos(EmpregosDic)