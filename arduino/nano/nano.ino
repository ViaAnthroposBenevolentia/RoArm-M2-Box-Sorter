// Arduino Nano code for conveyor belt control with box detection

// Pin Definitions
#define MOTOR_EN 9     // PWM pin for motor speed control
#define MOTOR_IN1 5    // Motor direction control pin 1
#define MOTOR_IN2 6    // Motor direction control pin 2

#define TRIG_PIN 2     // Ultrasonic sensor trigger pin
#define ECHO_PIN 3     // Ultrasonic sensor echo pin

// Distance Threshold (in centimeters)
const long DISTANCE_THRESHOLD = 6; // Adjust this value based on your setup

// Flag to indicate if a box has been detected and is being processed
bool boxProcessed = false;

void setup() {
  // Initialize Serial Communication at 9600 baud
  Serial.begin(9600);
  while (!Serial) {
    ; // Wait for serial port to connect. Needed for native USB
  }
  Serial.println("Arduino Nano Initialized");

  // Initialize Motor Control Pins
  pinMode(MOTOR_EN, OUTPUT);
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);

  // Initialize Ultrasonic Sensor Pins
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Start the Conveyor Motor
  startMotor();
}

void loop() {
  // If a box has not been processed yet, check for detection
  if (!boxProcessed) {
    float distance = readDistance();
    // Uncomment the next line for debugging distance readings
    // Serial.print("Distance: "); Serial.println(distance);
    
    if (distance > 0 && distance < DISTANCE_THRESHOLD) {
      // Box detected
      Serial.println("box_detected");
      stopMotor();
      boxProcessed = true; // Prevent multiple detections for the same box
    }
  }

  // Check for incoming serial data from Python script
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim(); // Remove any trailing newline or spaces

    // Uncomment the next lines for debugging incoming messages
    // Serial.print("Received: ");
    // Serial.println(message);
    
    if (message == "arm_done") {
      // Arm has completed processing the box
      Serial.println("Received 'arm_done'. Restarting conveyor.");
      startMotor();
      boxProcessed = false; // Reset flag for next box
    }
  }

  // Small delay to prevent overwhelming the serial buffer
  delay(100);
}

// Function to read distance from ultrasonic sensor
float readDistance() {
  // Clear the TRIG_PIN by setting it LOW for 2 microseconds
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  // Trigger the sensor by setting TRIG_PIN HIGH for 10 microseconds
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read the ECHO_PIN, returns the sound wave travel time in microseconds
  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // Timeout after 30ms (approx 510 cm)

  if (duration == 0) {
    // No echo received
    return -1;
  }

  // Calculate the distance in centimeters
  float distance = (duration * 0.034) / 2.0; // Speed of sound wave divided by 2 (go and return)
  return distance;
}

// Function to start the conveyor motor
void startMotor() {
  // Set motor direction: IN1 HIGH, IN2 LOW for forward motion
  digitalWrite(MOTOR_IN1, LOW);
  digitalWrite(MOTOR_IN2, HIGH);
  
  // Set motor speed to full (140). Adjust PWM value as needed
  analogWrite(MOTOR_EN, 120);
  
  Serial.println("Motor started");
}

// Function to stop the conveyor motor
void stopMotor() {
  // Stop the motor by setting ENA to 0 and direction pins LOW
  analogWrite(MOTOR_EN, 0);
  digitalWrite(MOTOR_IN1, LOW);
  digitalWrite(MOTOR_IN2, LOW);
  
  Serial.println("Motor stopped");
}
