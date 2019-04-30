import React, { Component } from 'react'
import axios from 'axios'
import ErrorNotification from './ErrorNotification'

class AddGame extends Component {
    state = {
        title: '',
        maxPlayers: '',
        minPlayers: '',
        errorMessage: ''
    }

    constructor() {
        super()

        this.onChange = this.onChange.bind(this)
        this.addGame = this.addGame.bind(this)
        this.clearForm = this.clearForm.bind(this)
        this.closeError = this.closeError.bind(this)
        this.cancelClick = this.cancelClick.bind(this)
    }

    onChange = function (e) {
        this.setState({ [e.target.name]: e.target.value })
    }

    addGame = () => {
        let data = {
            title: this.state.title,
            minPlayers: this.state.minPlayers,
            maxPlayers: this.state.maxPlayers
        }

        axios.post('http://127.0.0.1:8080/game/add', data).then((resp) => {
            this.clearForm()
            if (this.props.onGameAdded) {
                this.props.onGameAdded()
            }
        }).catch((err) => {
            this.setState({errorMessage: 'There was a problem adding your board game'})
        })
    }

    clearForm = () => {
        this.setState({
            title: '',
            maxPlayers: '',
            minPlayers: '',
            errorMessage: ''
        })
    }

    cancelClick = () => {
        this.clearForm()
        if (this.props.onCancelClicked) {
            this.props.onCancelClicked()
        }
    }

    closeError = () => {
        this.setState({errorMessage: ''})
    }

    render() {
        let errorNotification = null
        if (this.state.errorMessage) {
            errorNotification = <ErrorNotification message={this.state.errorMessage} onClose={this.closeError} />
        }

        return (
            <div>
                {errorNotification}

                <div className="field">
                    <label className="label">Title</label>
                    <div className="control">
                        <input className="input" type="text" name="title"
                            placeholder="Title" value={this.state.title}
                            onChange={this.onChange}></input>
                    </div>
                </div>

                <div className="field">
                    <label className="label">Max Players</label>
                    <div className="control">
                        <input className="input" type="text" name="maxPlayers"
                            placeholder="Max Players" value={this.state.maxPlayers}
                            onChange={this.onChange}></input>
                    </div>
                </div>

                <div className="field">
                    <label className="label">Min Players</label>
                    <div className="control">
                        <input className="input" type="text" name="minPlayers"
                            placeholder="Min Players" value={this.state.minPlayers}
                            onChange={this.onChange}></input>
                    </div>
                </div>

                <div className="field is-grouped">
                    <div className="control">
                        <button className="button is-link" onClick={this.addGame}>Submit</button>
                    </div>
                    <div className="control">
                        <button className="button is-text" onClick={this.cancelClick}>Cancel</button>
                    </div>
                </div>
            </div>)
    }
}

export default AddGame
