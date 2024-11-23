<p style="text-align: right;"><em>DATE: JANUARY - JUNE 2024</em></p>

# **PROJECT UNIT NUMBER ONE**

## **Shortest route to make**

### Made In: Python

#### Activity number: 14

#### **DESCRIPTION:**

#### For this activity, we have to create the base project to iterate in future using machine learning

________________________________________________________
________________________________________________________

#### Student: José López Lara

#### Control Number: 19120194

* [x] Student Email: <l19120194@morelia.tecnm.mx>
* [x] Personal Email: <jose.lopez.lara.cto@gmail.com>
* [x] GitHub Profile: [JoseLopezLara](https://github.com/JoseLopezLara)
* [x] Linkedin Profile: [in/jose-lopez-lara/](https://www.linkedin.com/in/jose-lopez-lara/)

________________________________________________________
________________________________________________________

### **STEP ONE: Run project and add 3 balls**

**Test: We can show the multiple balls**
![image](image1.png)

### **STEP TWO: Seva data recopiled in csv format and plot this data**

**Test: We can view the data for 1 ball**
![image](image2.png)

**Test: We can view the data for 1 ball**
**Test: We can view the data for 1 ball**

### **STEP THREE: Thinking what data I need to get about ball number 2 and number three to generate data set by each one**

#### **User Moves labels**

| Label  | Action  |
|--------|---------|
|0 0     |Quieto   |
|0 1     |Salto    |
|1 0     |Izquierda|
|1 1     |Derecha  |

#### **For Horizontal ball**

| Desp X Bala | Velocidad bala | Etiqueta|
|-------------|----------------|---------|

#### **For vertical ball**

|Desp X Jugador | Desp X Bala | Desplazamiento Y Bala | Velocidad bala | Etiqueta|
|---------------|-------------|-----------------------|----------------|---------|

#### **For diagonal ball**

|Desp X Jugador | Desp X Bala | Desplazamiento Y Bala | Velocidad bala | Etiqueta|
|---------------|-------------|-----------------------|----------------|---------|

**DUDA:**
Las dudas nacen a partir de que el humano (Creo yo JAJAJA), decide moversee o no desde una visión general que
tiene de la trayectoria del objeto. El humano predice si un objeto le puede pegar o no, pero esto lo hace en base el
analisis del punto de choque, no al analizar la trayectoria continua del objeto  

1. Tengo la duda si el ¿Punto de choque puede ayudar a que el modelo sea mas eficiente?
2. ¿El punto de choque aporta valor de la misma manera que la velocidad de vala?
3. ¿El punto de choque puedo sustuir el Desplazamiento diagonal?
4. ¿Si el punto de choque es mejor, debria añadirlo cuando la valar sale desde una posición vertical?
|Desp X Jugador | Desp Diagonal Bala | Velocidad bala | Punto de choque | Etiqueta |
|---------------|-------------|-----------------------|----------------|---------|

**Test: Data sets generated**
![image](image1.png)

### **CODE**

```python

```
