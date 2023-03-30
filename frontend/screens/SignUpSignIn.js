import React, {useState} from 'react';
import { StyleSheet, Image, Text, View, SafeAreaView, TouchableOpacity, TextInput } from 'react-native';
import InputTextField from '../components/InputTextField';


const SignUpSignIn = ({ navigation }) => {
  const [email, setEmail]=useState("")
  const [password, setPassword]=useState("")
  
  function retrieveTargets(resp) {
    console.log(resp)
    console.log(typeof resp)

    const userId=resp[0]
    const userName=resp[1]
    const userEmail=resp[2]

    const url = 'http://10.239.101.190:5000/targets/'+userId+'/'
    console.log(url)
    return fetch(url, {
      method: "GET",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
      .then((resp) => resp.json())
      .then((data) => {
        navigation.navigate('HomeScreen', {
          userName: userName,
          userEmail: userEmail,
          userId: userId,
          targets: data,
        })

        return data})
        
      .catch((error) => {
        console.error("Error fetching data:", error);
        return [];
        });}
  
  
        function signIn() {

          console.log("email")
          console.log(email)
          const url = 'http://10.239.101.190:5000/users/'+email
          return fetch(url, {
            method:'POST',
            headers:{
                'Accept':'application/json',
                'Content-Type':'application/json'
            },
            body:JSON.stringify({
              password:password})} //ADD SECURITY. I DONT LIKE TO SEND PASSWORD TO LOCAL HOST
            )
            
            .then(resp => {
              if (resp === "Incorrect password") {
                console.log(resp);
              ;
              }
              else if (resp==="User Does Not Exist"){
                
                console.log(resp);
              }
              else {
                console.log("next stop cov")
                console.log(resp.value)
                return resp.json() // Convert the response to JSON
              }
            })
            .then(json => {
              retrieveTargets(json); // Pass the JSON response to the retrieveTargets function
            })
            .catch((error) => {
              console.error("Error fetching data:", error);
              return [];
            });
        }

  return (
    <SafeAreaView style={styles.container}>
          <Image style={styles.wfLogo} resizeMode="contain" source={require('./logo_dark.png')}/>

          <View>
              <TouchableOpacity>
                  <View style={styles.socialButton}>
                    <Image style={styles.logo} source={require('./google_logo.jpeg')}/>
                    <Text style={styles.buttonText}>Google</Text>
                  </View>
              </TouchableOpacity>
          </View>

          <Text style={[styles.buttonText, { textAlign: "center", marginVertical: 10 }]}>or</Text>

          <View>
              <Text style={styles.inputTitle}>Email</Text>
              <TextInput
                style={styles.input}
                value={email}
                onChangeText = {text=>setEmail(text)} 
                keyboardType="default"
                ></TextInput>
              <View style={{ width: 250, borderBottomWidth: 1, borderBottomColor: "#FFF"}}></View>
          </View> 

          <View style={{ marginTop: 10}}>
              <Text style={styles.inputTitle}>Password</Text>
              <TextInput
                style={styles.input}
                value={password}
                onChangeText = {text=>setPassword(text)} 
                keyboardType="default"
                ></TextInput>
              <View style={{ width: 250, borderBottomWidth: 1, borderBottomColor: "#FFF"}}></View>
          </View> 


          <TouchableOpacity>
            <Text style={[styles.buttonText, { marginLeft: 10, fontWeight: "600" }]}>Forgot Password?</Text>
          </TouchableOpacity>
          
          
          <TouchableOpacity style={styles.buttons} onPress={() => signIn()}>
              <Text style={styles.buttonText}>Login</Text>
          </TouchableOpacity>
          
          <View style={{ marginTop: 10 }}>
            <Text style={styles.buttonText}>
                Don't have an account?   
                <TouchableOpacity onPress={() => navigation.navigate('SignUp')}>
                    <Text style={[styles.buttonText, { fontWeight: "600", marginTop: 15 }]}> Register Now</Text>
                </TouchableOpacity>
            </Text>
          </View> 
    </SafeAreaView>
  );
}

export default SignUpSignIn;

const styles = StyleSheet.create({
  inputTitle: {
    color: "#FFF", 
    fontSize: 14
    },
    input: {
        paddingVertical: 12,
        color: "#FFF", 
        fontSize: 14, 
        fontFamily: "Avenir Next"
    },
    container: {
      flex: 1,
      backgroundColor: '#000',
      alignItems: "center"
    },
    buttons: {
        fontSize: 16,
        borderRadius: 4, 
        marginTop: 30, 
        paddingVertical: 7,
        paddingHorizontal: 20,
        alignItems: "center", 
        backgroundColor:'#68a0cf',
        justifyContent: "center",
        shadowColor: "rgba(171, 180, 189, 0.35)",
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.5,
        shadowRadius: 10,
        elevation: 5
    },
    wfLogo: {
      top: 100,
      height: 100,
      width: 350
    },
    logo: {
      height: 18,
      width: 20,
      marginRight: 8
    },
    socialButton: {
        marginTop: 150, 
        flexDirection: "row",
        marginHorizontal: 12,
        paddingVertical: 12,
        paddingHorizontal: 30,
        borderWidth: StyleSheet.hairlineWidth, 
        borderColor: "#FFF", 
        borderRadius: 4,
        backgroundColor: "#000",
        shadowColor: "rgba(171, 180, 189, 0.35)",
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.5,
        shadowRadius: 10,
        elevation: 5
    },
    buttonText: {
        fontFamily: "Avenir Next", 
        color: "#FFF"
    }
  });
