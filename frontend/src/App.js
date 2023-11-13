import {React, useState} from 'react';
import axios from 'axios'

function Header () {
  return (
    <header>
      Script Ideas
    </header>
  );
}

function Form () {
  const [businessName, setBusinessName] = useState("");
  const [description, setDescription] = useState("");
  const [inference, setInference] = useState("");

  function handleSubmit(e){
    e.preventDefault();
    console.log(businessName, description);
    setInference(businessName + description);

    axios.get('http://localhost:8081/check_api_health')
      .then((response) => console.log(response))
      .catch((error) => console.log(error));

    axios.post('http://localhost:8081/generate_script', 
    {
      "name": businessName,
      "description": description
    })
    .then((response) => {
      console.log(response);
      setInference(response.data); // Assuming response data contains the script
    })
    .catch((error) => {
      console.error("Error fetching data: ", error);
      setInference("Error in generating script.");
    });
  }

  return (
    <div className="input-section">
      <form onSubmit={handleSubmit}>
        <input type="text" id="business_name" placeholder="Business Name" onChange={(e)=>setBusinessName(e.target.value)}/>
        <input type="textarea" placeholder="Description" onChange={(e)=>setDescription(e.target.value)}/>
        <button type="submit">Generate Script Ideas</button>
      </form>
      <div className="output-section">
        <p style={{'white-space': 'pre-line'}}>{inference}</p>
      </div>
    </div>
  );
}

function App() {

  return (
    <>
      <Header />
      <Form />
    </>
  );
}

export default App;
