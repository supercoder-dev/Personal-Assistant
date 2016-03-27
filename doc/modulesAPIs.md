# Module's API definitions #

All modules communicate with the kernel by strictly defined API. All modules are executed as separate processes and therefore interprocess communication is needed. In this project we have decided to use the [ZeroMQ](http://zeromq.org/) library to provide this communication. All transfered messages are the [JSON](http://www.ecma-international.org/publications/files/ECMA-ST/ECMA-404.pdf) format.

### Standard request: kernel &rarr; module ###
    {
        "config":
            {...},
        "data":
            {...},
        "timestamp": "2016-01-21 21:21:21"
    }

Content of the fields *"data"* and *"config"* is specified in details seprately for each module. Each field can be empty if no *"data"* or *"config"* is sent.

### Standard reply: module &rarr; kernel ###
    {
        "config":
            {
                "state": "accepted"|"failed"
            },
        "data":
            {...},
        "timestamp": "2016-01-21 21:21:21"
    }

Field *"state"* is *"accepted"* when configuration of the module went well or *"failed"* when some data is missing or wrong values are given. Content of the field *"data"* is specified for each module separately.

## Attention word module ##
  * **Request**
    * `config`:
      * `attentionWord`: string, phrase that wake up the system
      * `threshold`:
    * `data`:
      * `action`: string `listen` to start listening for the attention word
  * **Reply**
    * `data`:
      * `timeOfActivation`: timestamp, when the attention word was heard and recognized (eg. string `2016-01-01 21:21:21`)


