import React from "react";

class myComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { data: null };
  }

  componentDidMount() {
    const apiUrl = "http://127.0.0.1:5000/";
    var component = this;
    fetch(apiUrl)
      .then((response) => {
        return response.json();
        // return myData;
      })
      .then((json) => {
        component.setState({
          data: JSON.stringify(json),
        });
        console.log("parsed json", json);
      })
      .catch((ex) => {
        console.log("parsing failed", ex);
      });
    console.log(this.state.data);
  }

  render() {
    return <p>{this.state.data}</p>;
  }
}

export default myComponent;
