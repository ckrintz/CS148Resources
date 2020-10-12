import React, { useState } from 'react';

function CredsForm(props) {
    //The hard brackets are "array deconstruction" operator
    //updateState (name it anything you want) is a function we'll use to update this state object below
    const [state, updateState] = useState({
        acckey: "",
        seckey: ""
    })
    //Remember that updating state means we make a complete new copy and overwrite the exisiting state
    //Remember that React.useState on state objects requires that we copy the existing state upon each update (using the "spread" operator ...state) -- see below

    function handleChange(evt) { //updating form elements, nested function
        const name = evt.target.name //defined in render
        const value = evt.target.value //defined in render
	//because we are using a single state object above to hold multiple properties, we must save off the current state first (b/c we are only updating part of the object).  To do this, we "spread" state via ...state and add it to the new copy of state that updateState is creating, followed by any updates we want:
	updateState({
            ...state,
            [name]: value
        })
}

    const saveCreds = (evt) => {  //send creds to backend, nested arrow function
	evt.preventDefault();
        alert(`Submitting ${state.acckey} and ${state.seckey}`)
	
        let server = "http://localhost:8118/api"
        if (process.env.REACT_APP_REMOTE) { //set this in .env file: REACT_APP_REMOTE=1
            server = "https://cjk-flasktest.herokuapp.com/api"
	}
        if (process.env.NODE_ENV !== 'development') {
            server = "https://cjk-flasktest.herokuapp.com/api"
	}
	console.log("server = "+server)
        const url = `${server}/keys`
	const bd = JSON.stringify({ "acckey":state.acckey, "seckey":state.seckey })
        fetch(url, {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },           
            body: bd     
	  }).then(response => response.json()) 
	  .then(data => {
		  console.log("SaveCreds saveCreds: Fetch Response data: ")
		  console.log(data) //don't log an object WITH a string else the conversion won't work and object will not be dumped
		  alert('response: ' + data["MESSAGE"])
	  }).catch((error) => console.log("SaveCreds saveCreds: Fetch Failure (is server up?): "+ error))
    }

    //See this example on Creating Custom Hooks at  https://rangle.io/blog/simplifying-controlled-inputs-with-hooks/ to preclude the need to add a function handleChange for each onChange event
    return (
      <div> {/* JSX comments look like this */}
      {/*print out the NODE_ENV set by the server and our user defined REACT_APP_REMOTE variable value (no value means its undefined) */}
      <h3>Server: {process.env.NODE_ENV}, REACT_APP_REMOTE = {process.env.REACT_APP_REMOTE} </h3>
      <form onSubmit={saveCreds}>
        <label>
          Access Key:
          <input 
	    type="text" 
	    value={state.acckey} 
	    name="acckey" 
	    onChange={handleChange} />
        </label>
        <label>
          Secret Key:
          <input 
	    type="text" 
	    value={state.seckey} 
	    name="seckey" 
	    onChange={handleChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>
      </div>
    )
}
export default CredsForm;
