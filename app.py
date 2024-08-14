 from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

def calcular_tmb(peso, altura, edad, genero):
    if genero == 'hombre':
        return 10 * peso + 6.25 * altura - 5 * edad + 5
    elif genero == 'mujer':
        return 10 * peso + 6.25 * altura - 5 * edad - 161

def calcular_get(tmb, nivel_actividad):
    factores_actividad = {
        'sedentario': 1.2,
        'ligero': 1.375,
        'moderado': 1.55,
        'intenso': 1.725,
        'muy_intenso': 1.9
    }
    return tmb * factores_actividad[nivel_actividad]

def generar_menu_semanal(calorias_diarias):
    comidas = ["Desayuno", "Almuerzo", "Cena", "Snack"]
    menu = {}
    for dia in range(7):
        menu[f"Día {dia + 1}"] = {comida: f"{random.randint(200, 500)} calorías" for comida en comidas}
    return menu

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calorias', methods=['POST'])
def calcular_calorias():
    data = request.json
    peso = data['peso']
    altura = data['altura']
    edad = data['edad']
    genero = data['genero']
    nivel_actividad = data['nivel_actividad']
    
    tmb = calcular_tmb(peso, altura, edad, genero)
    get = calcular_get(tmb, nivel_actividad)
    
    return jsonify({'calorias_diarias': get})

@app.route('/menu', methods=['POST'])
def obtener_menu():
    data = request.json
    calorias_diarias = data['calorias_diarias']
    menu = generar_menu_semanal(calorias_diarias)
    return jsonify(menu)

if __name__ == '__main__':
    app.run(debug=True)

