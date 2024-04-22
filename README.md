# Exercise: event-based chat

## Contents

1. Overview
2. Demo

## Overview

### Goals
1. Allow end-users to create channels with the hard delete option
2. Allow custom events that can be interpreted in any way by the UI clients

### How it works

![Diagram 1](images/EventBasedChat1.png)

With Solid, we can use the concept of "storage-local compute" to keep the components within the Pod Provider as shown below. Or it can also be in a distributed system. 

![Diagram 2](images/EventBasedChat2.png)

### Overview of my demo

- clients and server processes run locally on the same host. UI is on a terminal
- it is for illustrative purposes only to demo the concept

![Diagram 3](images/EventBasedChat3.png)

### Known issues with the concept

1. Users need to trust the Pod Provider (or a Trusted Listener)
  - for access to their data (event_log)
  - for correctly re-constructing the messages into generated_chat => integrity 
2. HTTP PATCH method may have a side effect? Although how the underlying data is stored on the server can be unknown to the client, so maybe it doesn't count as a side effect?
3. Unsure about performance issues - how it may scale or handle high frequency of events. 
  - Optimization in the Trusted Listener to efficiently generate the generated_chat file based on the latest event
  - Optimization in the client UI to efficiently process all events in the generated chat. Eg. Could add another "storage-local compute" component that only sends the diff of the generated chat to the client UI instead of the whole chat. 
4. Trusted Listener is needed to be reliable and always running, otherwise clients will not receive the latest updates. 