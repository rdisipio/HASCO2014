#define inPinPhotoDiode 0
#define inPinThermistor 5

double R1 = 10000.0; //resistance put in parallel
double V_IN = 5.0;

// Steinhart-Hart formula
double A = 1.129148e-3;
double B = 2.34125e-4;
double C = 8.76741e-8;
double K = 9.5; // mW/dec C – dissipation factor

double SteinhartHart(double R)
{
  // calculate temperature
  double logR  = log(R);
  double logR3 = logR * logR * logR;

  return 1.0 / (A + B * logR + C * logR3 );
}

void setup(void) {
 
  Serial.begin(9600);
}
 
void loop(void) {
   
  int pinRead0 = analogRead(inPinPhotoDiode);
  float V0 = pinRead0 / 1024.0 * V_IN;
   
  int pinRead5 = analogRead(inPinThermistor);
  float V5 = pinRead5 / 1024.0 * V_IN;
  
  //calculate resistance
  double R_th = ( R1 * V5 ) / ( V_IN - V5 );
  double Tkelvin = SteinhartHart(R_th) - V5*V5/(K * R_th);
  double Tcelsius = Tkelvin - 273.15;

/*
  Serial.print( "Photodiode volt = " );
  Serial.print( V0 );
  Serial.print( " / Thermistor volt = " );
  Serial.print( V5 );
  Serial.print( " / Temperature [C] = " );
  Serial.print( Tcelsius );
  Serial.println();
  */
  Serial.print( V0 );
  Serial.print( "," );
 // Serial.print( V5 );
 // Serial.print( "," );
  Serial.print( Tcelsius );
  Serial.println();
  
  delay(100);
   
}
