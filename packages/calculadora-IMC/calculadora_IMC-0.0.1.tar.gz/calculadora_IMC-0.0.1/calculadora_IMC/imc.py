def calcular_imc(peso, altura):
    imc = peso / altura**2
    return imc

def interpretar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 25:
        return "Peso normal"
    elif 25 <= imc < 30:
        return "Sobrepeso"
    else:
        return "Obeso"

def main():
    peso = float(input("Digite o seu peso (em kg): "))
    altura = float(input("Digite a sua altura (em metros): "))

    imc = calcular_imc(peso, altura)
    categoria = interpretar_imc(imc)

    print("Seu IMC é: {:.2f}".format(imc))
    print("Categoria: ", categoria)

if __name__ == "__main__":
    main()
