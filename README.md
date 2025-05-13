# Happy Surveillance  
*A Hack-A-Bot 2025 Project*

## Overview
**Happy Surveillance** is a prototype security gate system developed during **Hack-A-Bot 2025**. The challenge was to leverage a **Raspberry Pi 5** and **Sony AI camera** to improve campus security. Our team built a system that uses **facial recognition** and **emotion detection** to verify individuals and assess emotional state at access points.

If a person is **not recognized** in the database or is **not exhibiting a positive facial expression**, access is denied. As part of the physical deterrent system, a **motorized spring-loaded arm hits the person in the shins**, with a block of wood, to reinforce compliance with the security protocol.

## Project Goals
- Enhance access control with biometric and behavioral verification  
- Explore emotion detection as a factor in secure environments  
- Provide real-time data and analytics to campus security teams

## Web Dashboard
The MERN stack dashboard offers campus security personnel a centralized interface to:
- View real-time entry events  
- Monitor recognized and unrecognized individuals  
- Analyze emotion trends and system alerts  

## System Components

### Hardware
- Raspberry Pi 5  
- Sony AI Camera  
- Motorized Arm Actuator (for feedback)  

### Software
- Facial Recognition Model for identity verification  
- Emotion Classification Model to detect facial expressions  
- PoseNet for person alignment and positional awareness  
- **MERN Stack Dashboard**:
  - MongoDB  
  - Express.js  
  - React  
  - Node.js  

## Features
- Real-time facial recognition and emotion detection on edge  
- Physical response mechanism for failed access attempts  
- Web-based dashboard for monitoring and reviewing access logs  
- Analytics for tracking usage, entry attempts, and emotion patterns  
