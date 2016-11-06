// Constants which won't change. 
// They're used here to set pin numbers:
const int buttonPin = 2;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin
const int voltagepin = 6;    // the number of the pin for adjusting voltage

// Variables will change:
int buttonState = 0;              // variable for reading the pushbutton status
int devicerunning = 0;            // variable for reading the pushbutton status
float InitialVoltage = 0;         // variable for starting voltage value
float NewVoltage = InitialVoltage;
float PythonIntensity = 90;
float SPIntensity = 50;
float percentdifference = 0;

 
 
void setup() {
  Serial.begin(115200);
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
  pinMode(voltagepin, OUTPUT);

  // Set the initial voltage of the voltage pin
  // Multiple by 51 to get the number which Arudino needs
  analogWrite(voltagepin,51*InitialVoltage);
}

 
String GetNewVoltage(String readString) {   
 // Wait and don't do anything if the Serial is not avaiable
 // i.e., Python is currently writing a new number
  while(!Serial.available()) {}
  while (Serial.available())
  {
    if (Serial.available() > 0)
    {
      char c = Serial.read();  //Gets one byte from serial buffer
      readString += c; //Add to the string readString
    }
  }
  return readString;
}


void loop() {
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);
  
  // check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH:
  if (buttonState == HIGH) {
      if (devicerunning == 0){
        devicerunning = 1;
        // turn LED on:
         digitalWrite(ledPin, HIGH);
      } else {
  
        devicerunning = 0;
         // turn LED off:
      digitalWrite(ledPin, LOW);
      }
          
    delay(100);
    }

    if (devicerunning == 1){

    // Read New Voltage Value from Python
    
//    Serial.print('\n');
//    Serial.print("Getting new voltage from Python...");
  
    String readString; // Clear this variable now 
    for (int i=0; i <= 2; i++){
      readString = GetNewVoltage(readString);
//      delay(50);
    } 
    Serial.println(readString);
    
    NewVoltage = readString.toFloat(); // Convert from string to float 

    // Maximum voltage of arduino is 5 Volts (255) smallest is 0 volts (0)
    if (NewVoltage > 255){
      NewVoltage = 255;        
    }
    if (NewVoltage < 0){
      NewVoltage = 0;        
    }
    
    // Adjust voltage in pin
    analogWrite(voltagepin,51*NewVoltage);



    
    }
    

}
