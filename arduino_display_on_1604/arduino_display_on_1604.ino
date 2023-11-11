#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);  

void setup() 
{
  lcd.begin(16,4);

  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(1);
}

void loop() 
{
  // put your main code here, to run repeatedly:
  lcd.setCursor(0, 0);
  String line = readLine();
  lcd.print(line);
  delay(1000);
}

String readLine() 
{
  String readStrings = "";
  while (Serial.available() > 0)
  {
    char c = Serial.read();
    if (c == 'e' || c == '\n')
    {
      return readStrings;
    }
    readStrings += c;
  }
}
