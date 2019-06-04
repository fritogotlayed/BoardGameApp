import React, { Component } from 'react'
import axios from 'axios'
import GameGrid from './components/GameGrid'
import GameGridFilter from './components/GameGridFilter'
import AddGame from './components/AddGame'
import EditGame from './components/EditGame'

class Search extends Component {
    state = {
        // data: [],
        data: null,
        addingGame: false,
        editedGame: null,
        showFilterPanel: false
    }

    constructor() {
        super()

        this.loadGrid = this.loadGrid.bind(this)
        this.showModal = this.showModal.bind(this)
        this.hideModal = this.hideModal.bind(this)
        this.gameAdded = this.gameAdded.bind(this)
        this.onGridRowDelete = this.onGridRowDelete.bind(this)
        this.onGridRowEdit = this.onGridRowEdit.bind(this)
        this.onFilterApplied = this.onFilterApplied.bind(this)
        this.toggleFilterPanelState = this.toggleFilterPanelState.bind(this)
    }

    loadGrid = (filter) => {
        let filterQuery = ''
        if (filter) {
            filterQuery += '?'
            if (filter['title']) {
                filterQuery += 'title=' + escape(filter['title'])
            }

            if (filter['maxPlayers']) {
                if (filter['title']) {
                    filterQuery += '&'
                }

                filterQuery += 'maxPlayers=' + escape(filter['maxPlayers'])
            }

            if (filter['minPlayers']) {
                if (filter['maxPlayers']) {
                    filterQuery += '&'
                }

                filterQuery += 'minPlayers=' + escape(filter['minPlayers'])
            }
        }

        fetch('http://127.0.0.1:8080/game' + filterQuery)
            .then(response => response.json())
            .then(data => this.setState({ data: data.data }))
            .then(this.setState({showFilterPanel: false}));
    }

    showModal = () => {
        this.setState({addingGame: true})
    }

    hideModal = () => {
        this.setState({addingGame: false, editedGame: null})
    }

    gameAdded = () => {
        this.hideModal()
        this.loadGrid()
    }

    gameEdited = () => {
        this.hideModal()
        this.loadGrid()
    }

    onGridRowEdit = (key) => {
        var editedItem = this.state.data.find((elem) => {
            return elem._key === key
        })

        if (editedItem) {
            this.setState({editedGame: editedItem})
        }
    }

    onGridRowDelete = (key) => {
        axios.delete('http://127.0.0.1:8080/game/' + key + '/delete').then((resp) => {
            this.loadGrid()
        }).catch((err) => {
            console.log(err)
        })
    }

    onFilterApplied = (data) => {
        this.loadGrid(data)
    }

    componentDidMount() {
        this.loadGrid()
    }

    toggleFilterPanelState() {
        this.setState({showFilterPanel: !this.state.showFilterPanel})
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
        } else if (this.state.editedGame) {
            modal = (
                <div className="modal is-active">
                    <div className="modal-background"></div>
                    <div className=">modal-content">
                        <div className="box">
                            <EditGame gameToEdit={this.state.editedGame} onGameEdited={this.gameEdited} onCancelClicked={this.hideModal} />
                        </div>
                    </div>
                    <button className="modal-close is-large" aria-label="close" onClick={this.hideModal}></button>
                </div>
            )
        }

        if (this.state.data) {
            return (
                <div style={{'marginLeft': '5%', 'width': '90%'}}>
                    {modal}
                    <div className={'dropdown' + (this.state.showFilterPanel ? ' is-active' : '')} style={{'marginTop': '0.5em'}}>
                        <div className="dropdown-trigger">
                            <button className="button" aria-haspopup="true" aria-controls="dropdown-menu4" onClick={this.toggleFilterPanelState}>
                                <span>Filter Results</span>
                            </button>
                        </div>
                        <div className="dropdown-menu" id="dropdown-menu4" role="menu">
                            <div className="dropdown-content">
                                <div className="dropdown-item">
                                    <GameGridFilter onFilterApplied={this.onFilterApplied}/>
                                </div>
                            </div>
                        </div>
                    </div>
                    <GameGrid style={{'width': '100%'}} data={this.state.data} onDeleteClick={this.onGridRowDelete} onEditClick={this.onGridRowEdit} />
                    <div className="field is-grouped is-grouped-right">
                        <p className="control">
                            <button className="button is-primary" onClick={this.showModal}>Add Game</button>
                        </p>
                    </div>
                </div>
            )
        } else {
            return (
                <div style={{'marginLeft': '5%', 'marginTop': '0.5em', 'width': '90%'}}>
                    <article class="message is-warning">
                        <div class="message-header">
                            <p>Warning</p>
                        </div>
                        <div class="message-body">
                            The system appears to be unavailable right now. Please try again later.
                        </div>
                    </article>
                </div>
            )
        }
    }
}

export default Search
