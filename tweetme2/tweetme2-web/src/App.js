import React,{useEffect,useState} from 'react';
import logo from './logo.svg';
import './App.css';


function loadTweets(callback){
        
  const xhr=new XMLHttpRequest()
  const method ='GET'  //"POST"
  const url="/api/tweets"
  const responseType="json"
  xhr.responseType = responseType
  xhr.open(method,url)
 

  xhr.onload =function(){
    callback(xhr.response, xhr.status)
 

  //console.log(listedItems)
}
xhr.send()

}


function App() {
  const [tweets, setTweets]=useState([])

  
  
  useEffect(()=>{
    const myCallback = (response,status)=>{
    
    setTweets(response)
    }
    loadTweets(myCallback)
   
  },[])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p>
          {tweets.map((tweet, index)=>{
            return <li>{tweet.content}</li>
          })}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
