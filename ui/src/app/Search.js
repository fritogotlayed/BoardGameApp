import React, { Component } from 'react'
import axios from 'axios'
import GameGrid from './components/GameGrid'
import AddGame from './components/AddGame'

class Search extends Component {
    state = {
        data: [],
        addingGame: false
    }

    constructor() {
        super()

        this.loadGrid = this.loadGrid.bind(this)
        this.showModal = this.showModal.bind(this)
        this.hideModal = this.hideModal.bind(this)
        this.gameAdded = this.gameAdded.bind(this)
        this.onGridRowDelete = this.onGridRowDelete.bind(this)
        this.onGridRowEdit = this.onGridRowEdit.bind(this)
    }

    loadGrid = () => {
        fetch('http://127.0.0.1:8080/game')
            .then(response => response.json())
            .then(data => this.setState({ data: data.data }));
    }

    showModal = () => {
        this.setState({addingGame: true})
    }

    hideModal = () => {
        this.setState({addingGame: false})
    }

    gameAdded = () => {
        this.hideModal()
        this.loadGrid()
    }

    onGridRowEdit = () => {
    }

    onGridRowDelete = (key) => {
        axios.delete('http://127.0.0.1:8080/game/' + key + '/delete').then((resp) => {
            this.loadGrid()
        }).catch((err) => {
            console.log(err)
        })
    }

    componentDidMount() {
        this.loadGrid()
    }

    render() {
        let modal = null
        if (this.state.addingGame) {
            modal = (
                <div className="modal is-active">
                    <div className="modal-background"></div>
                    <div className="modal-content">
                        <div className="box">
                            <AddGame onGameAdded={this.gameAdded} onCancelClicked={this.hideModal} />
                        </div>
                    </div>
                    <button className="modal-close is-large" aria-label="close" onClick={this.hideModal}></button>
                </div>
            )
        }

        return (
            <div>
                {modal}
                <button className="button is-primary" onClick={this.showModal}>Add Game</button>
                <GameGrid data={this.state.data} onDeleteClick={this.onGridRowDelete} onEditClick={this.onGridRowEdit} />
            </div>
        )
    }
}

export default Search