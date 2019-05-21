import React, { Component } from 'react'

class GameGridFilter extends Component {
    state = {
        title: '',
        maxPlayers: '',
        minPlayers: '',
        errorMessage: ''
    }

    constructor() {
        super()

        this.onChange = this.onChange.bind(this)
    }

    onChange = function (e) {
        this.setState({ [e.target.name]: e.target.value })
    }

    clearForm = () => {
        this.setState({
            title: '',
            maxPlayers: '',
            minPlayers: ''
        })
    }

    cancelClick = () => {
        this.clearForm()
        if (this.props.onCancelClicked) {
            this.props.onCancelClicked()
        }
    }

    filterApplied = () => {
        if (this.props.onFilterApplied) {
            this.props.onFilterApplied(this.state)
        }
    }

    render() {

        return (
            <div>
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
                        <button className="button is-text" onClick={this.clearForm}>Clear</button>
                    </div>
                    <div className="control">
                        <button className="button is-link" onClick={this.filterApplied}>Filter</button>
                    </div>
                </div>
            </div>)
    }
}

export default GameGridFilter
