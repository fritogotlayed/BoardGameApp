import React, { Component } from 'react'
import GameGrid from './components/GameGrid'
import AddGame from './components/AddGame'

class Search extends Component {
    state = {
        data: [
        ]
    }

    constructor() {
        super()

        this.loadGrid = this.loadGrid.bind(this)
    }

    loadGrid = () => {
        fetch('http://127.0.0.1:8080/game')
            .then(response => response.json())
            .then(data => this.setState({ data: data.data }));
    }

    componentDidMount() {
        this.loadGrid()
    }

    render() {
        return (
            <div>
                <p>This is the Search Page</p>
                <AddGame />
                <GameGrid data={this.state.data} />
            </div>
        )
    }
}

export default Search
