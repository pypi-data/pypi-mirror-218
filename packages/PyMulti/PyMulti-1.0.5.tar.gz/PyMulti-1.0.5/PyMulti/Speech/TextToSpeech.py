# PyMulti (Speech) - TextToSpeech

''' This is the "TextToSpeech" module. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import pyttsx3

# Function 1 - Get Property
def get_property(property, driver=None, debug=False):
    # Variables
    properties = ["rate", "voice", "voices", "volume", "pitch"]
    drivers = ["sapi5", "nsss", "espeak"]

    # Checking the Data Type of "property"
    if (isinstance(property, str)):
        # Checking if "property" is Valid
        if (property in properties):
            # Checking the Data Type of "driver"
            if (isinstance(driver, str) or (driver == None)):
                # Checking the Data Type of "debug"
                if (isinstance(debug, bool)):
                    # Checking if "driver" is None
                    if (driver == None):
                        # Creating the Engine
                        engine = pyttsx3.init(debug=debug)
                    else:
                        # Checking if "driver" is Valid
                        if (driver in drivers):
                            # Creating the Engine
                            engine = pyttsx3.init(driverName=driver, debug=debug)
                        else:
                            raise Exception("The 'driver' argument must be a valid driver's name. The available drivers are:\n\n" + str(drivers))

                    # Try/Except
                    try:
                        # Fetching the Property
                        fetchedProperty = engine.getProperty(property)

                        # Stopping the Engine
                        engine.stop()

                        # Returning the Property
                        return fetchedProperty
                    except:
                        raise Exception("Failed to fetch the '" + property + "' property.")
                else:
                    raise TypeError("The 'debug' argument must be a boolean.")
            else:
                raise TypeError("The 'driver' argument must be a string.")
        else:
            raise Exception("The 'property' argument must be a valid property's name. The available properties are:\n\n" + str(properties))
    else:
        raise TypeError("The 'property' argument must be a string.")

# Function 2 - Say
def say(text, rate=200, voice=get_property("voices")[0].id, volume=1.0, pitch=0.5, onStart=None, onWordStart=None, onWordEnd=None, onEnd=None, onError=None, driver=None, debug=False):
    # List of Drivers
    drivers = ["sapi5", "nsss", "espeak"]

    # Checking the Data Type of "text"
    if (isinstance(text, str)):
        # Checking the Data Type of "rate"
        if (isinstance(rate, int)):
            # Checking the Data Type of "voice"
            if (isinstance(voice, str)):
                # Checking the Data Type of "volume"
                if (isinstance(volume, float)):
                    # Checking the Data Type of "pitch"
                    if (isinstance(pitch, float)):
                        # Checking the Data Type of "driver"
                        if (isinstance(driver, str) or (driver == None)):
                            # Checking the Data Type of "debug"
                            if (isinstance(debug, bool)):
                                # Checking if "driver" is None
                                if (driver == None):
                                    # Creating the Engine
                                    engine = pyttsx3.init(debug=debug)
                                else:
                                    # Checking if "driver" is Valid
                                    if (driver in drivers):
                                        # Creating the Engine
                                        engine = pyttsx3.init(driverName=driver, debug=debug)
                                    else:
                                        raise Exception("The 'driver' argument must be a valid driver's name. The available drivers are:\n\n" + str(drivers))

                                # Try/Except
                                try:
                                    # Setting the Events
                                    if ((onStart != None) and (callable(onStart))):
                                        engine.connect("started-utterance", onStart)

                                    if ((onWordStart != None) and (callable(onWordStart))):
                                        engine.connect("started-word", onWordStart)

                                    if ((onWordEnd != None) and (callable(onWordEnd))):
                                        engine.connect("finished-word", onWordEnd)

                                    if ((onEnd != None) and (callable(onEnd))):
                                        engine.connect("finished-utterance", onEnd)

                                    if ((onError != None) and (callable(onError))):
                                        engine.connect("error", onError)

                                    # Setting the Properties
                                    engine.setProperty("rate", rate)
                                    engine.setProperty("voice", voice)
                                    engine.setProperty("volume", volume)
                                    engine.setProperty("pitch", pitch)

                                    # Converting Text to Speech
                                    engine.say(text)
                                    engine.runAndWait()
                                except:
                                    raise Exception("Failed to convert the text to speech.")
                            else:
                                raise TypeError("The 'debug' argument must be a boolean.")
                        else:
                            raise TypeError("The 'driver' argument must be a string.")
                    else:
                        raise TypeError("The 'pitch' argument must be a float.")
                else:
                    raise TypeError("The 'volume' argument must be a float.")
            else:
                raise TypeError("The 'voice' argument must be a string.")
        else:
            raise TypeError("The 'rate' argument must be an integer.")
    else:
        raise TypeError("The 'text' argument must be a string.")

# Function 3 - Save
def save(text, path, rate=200, voice=get_property("voices")[0].id, volume=1.0, pitch=0.5, onStart=None, onWordStart=None, onWordEnd=None, onEnd=None, onError=None, driver=None, debug=False):
    # List of Drivers
    drivers = ["sapi5", "nsss", "espeak"]

    # Checking the Data Type of "text"
    if (isinstance(text, str)):
        # Checking the Data Type of "path"
        if (isinstance(path, str)):
            # Checking the Data Type of "rate"
            if (isinstance(rate, int)):
                # Checking the Data Type of "voice"
                if (isinstance(voice, str)):
                    # Checking the Data Type of "volume"
                    if (isinstance(volume, float)):
                        # Checking the Data Type of "pitch"
                        if (isinstance(pitch, float)):
                            # Checking the Data Type of "driver"
                            if (isinstance(driver, str) or (driver == None)):
                                # Checking the Data Type of "debug"
                                if (isinstance(debug, bool)):
                                    # Checking if "driver" is None
                                    if (driver == None):
                                        # Creating the Engine
                                        engine = pyttsx3.init(debug=debug)
                                    else:
                                        # Checking if "driver" is Valid
                                        if (driver in drivers):
                                            # Creating the Engine
                                            engine = pyttsx3.init(driverName=driver, debug=debug)
                                        else:
                                            raise Exception("The 'driver' argument must be a valid driver's name. The available drivers are:\n\n" + str(drivers))

                                    # Try/Except
                                    try:
                                        # Setting the Events
                                        if ((onStart != None) and (callable(onStart))):
                                            engine.connect("started-utterance", onStart)

                                        if ((onWordStart != None) and (callable(onWordStart))):
                                            engine.connect("started-word", onWordStart)

                                        if ((onWordEnd != None) and (callable(onWordEnd))):
                                            engine.connect("finished-word", onWordEnd)

                                        if ((onEnd != None) and (callable(onEnd))):
                                            engine.connect("finished-utterance", onEnd)

                                        if ((onError != None) and (callable(onError))):
                                            engine.connect("error", onError)

                                        # Setting the Properties
                                        engine.setProperty("rate", rate)
                                        engine.setProperty("voice", voice)
                                        engine.setProperty("volume", volume)
                                        engine.setProperty("pitch", pitch)

                                        # Saving the File
                                        engine.save_to_file(text, path)
                                        engine.runAndWait()
                                    except:
                                        raise Exception("Failed to save the file.")
                                else:
                                    raise TypeError("The 'debug' argument must be a boolean.")
                            else:
                                raise TypeError("The 'driver' argument must be a string.")
                        else:
                            raise TypeError("The 'pitch' argument must be a float.")
                    else:
                        raise TypeError("The 'volume' argument must be a float.")
                else:
                    raise TypeError("The 'voice' argument must be a string.")
            else:
                raise TypeError("The 'rate' argument must be an integer.")
        else:
            raise TypeError("The 'path' argument must be a string and a valid file path.")
    else:
        raise TypeError("The 'text' argument must be a string.")