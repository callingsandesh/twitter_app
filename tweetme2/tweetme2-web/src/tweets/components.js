import React, {useEffect,useState} from 'react' 

export function TweetComponent(props){
  const textAreaRef = React.createRef()
  const [newTweets , setNewTweets] =useState([])
  const handleSubmit =(event)=>{
    event.preventDefault()
   
    const newValue = textAreaRef.current.value
    let tempNewTweets = [...newTweets] //copy the newTweets
    //change this to a server side call
    tempNewTweets.unshift({    //unshift put it to the very begining whereas push sends it to the last
      content:newValue,
      likes:0,
      id:12313
    })
    setNewTweets(tempNewTweets)
    textAreaRef.current.value=''
  }
  return <div className={props.classname}>
    <div className='col-12 mb-3'>
    <form onSubmit={handleSubmit}> 
    <textarea ref={textAreaRef} required={true} className='form-control'>


    </textarea>
    <button type="submit" className='btn btn-primary my-3'>Tweet</button>
  </form>
  </div>
  <TweetsList newTweets={newTweets}/>
  </div>
}
 
  
export function TweetsList(props){
    
      const [tweetsInit, setTweetsInit]=useState([])
      const [tweets, setTweets]=useState([])
      //setTweetsInit([...props.newTweets].concat(tweetsInit))
      
      useEffect(()=>{
        const final=[...props.newTweets].concat(tweetsInit)
        if (final.length !== tweets.length){
          setTweets(final)
        }
        
      },[props.newTweets,tweets, tweetsInit])

      useEffect(()=>{
        const myCallback = (response,status)=>{
          if(status === 200){
            
            setTweetsInit(response)
          }else{
            alert("Their was an error")
          }
        
        
        }
        loadTweets(myCallback)
       
      },[tweetsInit])
      return tweets.map((item, index)=>{
        return <Tweet tweet={item} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`}/>
      })
  }

function loadTweets(callback){
        
    const xhr=new XMLHttpRequest()
    const method ='GET'  //"POST"
    const url="http://localhost:8000/api/tweets/"
    const responseType="json"
    xhr.responseType = responseType
    xhr.open(method,url)
   
  
    xhr.onload =function(){
      callback(xhr.response, xhr.status)
   
  
    //console.log(listedItems)
  }
  xhr.onerror = function(e){
    console.log(e)
    callback({"message":"The request was an error"},400)
  }
  xhr.send()
  
  }

export function ActionBtn(props){
    const {tweet,action}=props
    const [likes,setLikes] = useState(tweet.likes ?tweet.likes :0)
    const [userLike,setUserLike]=useState(tweet.userLike === true ? true : false) 
    const className = props.className ? props.className : 'btn btn-outline-success btn-sm'
    const actionDisplay = action.display ? action.display :'Action'
    
    
    const handleClick=(event)=>{
        event.preventDefault()
        if (action.type === 'like'){
            if(userLike === true){
              //unlike
              setLikes(likes - 1)
              setUserLike(false)
            }else{
              setLikes(likes+1)
              setUserLike(true)

            }
            
            
        }
    }
    const display=action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    return <button className={className} onClick={handleClick}>{display}</button>
  }
  
export function Tweet(props){
    const{tweet}= props
    const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
    return <div className={className}>
      <p>{tweet.id}-{tweet.content}</p>
      <div className='btn btn-group'> 
        <ActionBtn tweet={tweet} action={{type:"like" , display:"Likes"}}/>
        <ActionBtn tweet={tweet} action={{type:"unlike", display:"UnLike"}}/>
        <ActionBtn tweet={tweet} action={{type:"retweet", display:"Retweet"}}/> 
      </div>
    </div>
  }