## **Onion-Server - Dot-Onion and hidden services manager and client**

---

Onion-Server provides a client for fast and easy hidden services management. Used for managing services in one session. Services include (.onion) deep web hosting on a local machine.
<br>

### **Installation**

```bash
python -m pip install onion-server
```

### **OS Support**

- Linux

### **Requirements**

onion-server requires tor services. Tor can be download using **apt**

```bash
$ apt install tor
```

<br>
<br>

## **USAGE**

---

**Running Onion-Server**

```bash
$ sudo onion
# or
$ sudo python -m onion_server
```

To run onion-server, type **sudo onion** or **sudo python -m onion_server** in the terminal and run.

<br>
<br>

## **COMMANDS**

---

### **server**

```bash
$ server.<command>
```

**start** - start server  
**stop** - stop server  
**scan** - scan server for unrecorded changes  
**reboot** | restart - restart or reboot server

<br>

### **tor**

```bash
$ tor.<command>
```

**start** - start tor service  
**stop** - stop tor service

<br>

### **http**

```bash
$ http.<command>
```

**start** - start http service  
**stop** - stop http service

<br>

### **web**

```bash
$ web.<command>
```

**info** - display web services status  
**dir** [ path ] - set new web files dir

```bash
$ web.dir <path>
```

**set** [ status ] - set web status

```bash
$ web.set <command>
```

**online** - set web service online  
**offline** - set web service offline

<br>

### **config**

```bash
$ config.<command>
```

**del** - delete config file  
**create** - create the config file

<br>

### **Others**

```bash
$ <command>
```

**reset** - reset server  
**scan** - update all running services on the server  
**status** - display server services status  
**help** - display help message  
**update** - update onion-server  
**exit** - quit server

<br>

---

<br>

> **NOTICE:** In case of any error or information email me. eirasmx@pm.me
