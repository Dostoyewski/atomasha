String s1 = "123456s";
String s2 = "654321s";
String s3 = "012301s";
String s4 = "069442s";
int is1, is2, is3, is4;

void setup() {
  Serial.begin(115200);
  delay(500);
}

void loop() {
  int a = random(0, 5);
  switch(a){
    case 1:{
      Serial.println(s1+is1);
      if(is1 == 0) is1 = 1;
      else is1 = 0;
      break;
    }
    case 2:{
      Serial.println(s2+is2);
      if(is2 == 0) is2 = 1;
      else is2 = 0;
      break;
    }
    case 3:{
      Serial.println(s3+is3);
      if(is3 == 0) is3 = 1;
      else is3 = 0;
      break;
    }
    case 4:{
      Serial.println(s4+is4);
      if(is4 == 0) is4 = 1;
      else is4 = 0;
      break;
    }
    
  }
  delay(5000);
}
