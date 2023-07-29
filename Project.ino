#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <SimpleTimer.h> 
#include <LCD.h>
#include <LiquidCrystal_I2C.h>


LiquidCrystal_I2C lcd(0x27, 2,1,0,4,5,6,7); 

volatile int Contador;  //variable que cuenta los pulsos

int PinSensor =2 ;

// Data wire is plugged into port 2 on the Arduino
#define ONE_WIRE_BUS 4

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);


// Pass our oneWire reference to Dallas Temperature.
DallasTemperature sensors(&oneWire);


void setup() {

  Serial.begin(9600);
  lcd.setBacklightPin(3, POSITIVE);
  lcd.setBacklight(HIGH);
  lcd.begin(16, 2); // inicializar el LCD con 16 columnas y 2 filas
  sensors.begin();
  pinMode(PinSensor, INPUT);
  attachInterrupt(0, pulso, RISING);
  Wire.begin();
  lcd.setCursor(0,0);
  lcd.print("Inicializando");delay(2000);lcd.clear();
}

void loop() {
  
  float ph = phSensor();
  Serial.print("imprimiendo el ph ");
  Serial.println(ph);
  delay(100);
  //waterTemperature();
  //waterFlow();
  
  lcd.setCursor(0,0);
  lcd.print("PH: ");
  lcd.setCursor(5,0);
  lcd.print(ph);

  waterTemperature();
  //waterFlow();
  
}

void waterTemperature() {
  Serial.print("Requesting temperatures...");
  sensors.requestTemperatures();  // Send the command to get temperatures
  Serial.println("DONE");
  // After we got the temperatures, we can print them here.
  // We use the function ByIndex, and as an example get the temperature from the first sensor only.
  float tempC = sensors.getTempCByIndex(0);

  // Check if reading was successful
  if (tempC != DEVICE_DISCONNECTED_C) {
    Serial.print("Temperature for the device 1 (index 0) is: ");
    Serial.println(tempC);
  } else {
    Serial.println("Error: Could not read temperature data");
  }
}
void pulso() {
  Contador++;
   
}
long funcion(void) {
  long cantidad;
  Contador = 0;
  interrupts();              //Se inician las interrupciones y se cuentan los pulsos
  noInterrupts();            //se suspenden las interrupciones
  cantidad = 10 * Contador;  // pulsos por segundo
  return cantidad;
}
void waterFlow() {

  float frecuencia = funcion();     //frecuencia de los pulsos
  float Caudal = frecuencia / 7.5;  //calculamos el caudal en L/m

  Serial.print("Litros por segundo: ");
  Serial.println(Caudal);
}



float phSensor() {

  SimpleTimer timer;

  float calibration_value = 21.34 - 0.7;
  int phval = 0;
  unsigned long int avgval;
  int buffer_arr[10], temp;
  float ph_act;


  timer.run();  // Initiates SimpleTimer
  for (int i = 0; i < 10; i++) {
    buffer_arr[i] = analogRead(A0);
    delay(30);
  }
  for (int i = 0; i < 9; i++) {
    for (int j = i + 1; j < 10; j++) {
      if (buffer_arr[i] > buffer_arr[j]) {
        temp = buffer_arr[i];
        buffer_arr[i] = buffer_arr[j];
        buffer_arr[j] = temp;
      }
    }
  }
  avgval = 0;
  for (int i = 2; i < 8; i++)
    avgval += buffer_arr[i];
  float volt = (float)avgval * 5.0 / 1024 / 6;
   return ph_act = -5.70 * volt + calibration_value;

    
    delay(1000);
}