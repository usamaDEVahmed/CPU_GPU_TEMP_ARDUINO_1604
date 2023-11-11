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
  lcd.setCursor(1, 0);
  lcd.print("usamaDEVahmed");

  String line = "";
  while (Serial.available() > 0)
  {
    char c = Serial.read();
    if (c == 'S')
    {
      lcd.setCursor(0, 2);
      lcd.print(line);;
      line = "";
    }
    else if (c == 'e')
    {
      lcd.setCursor(0, 3);
      lcd.print(line);
      line = "";
    }
    else 
    {
      line += c; 
    }
  }
  
  delay(1000);
}
