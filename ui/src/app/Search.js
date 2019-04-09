import React, { Component } from 'react'
import GameGrid from './components/GameGrid'

class Search extends Component {
    state = {
        data: [
        ]
    }

    componentDidMount() {
        fetch('http://127.0.0.1:8080/game')
            .then(response => response.json())
            .then(data => this.setState({ data: data.data }));
    }

    render() {
        return (
            <div>
                <p>This is the Search Page</p>
                <GameGrid data={this.state.data} />
            </div>
        )
    }
}

export default Search
