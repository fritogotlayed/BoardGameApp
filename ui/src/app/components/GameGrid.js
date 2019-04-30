import React, { Component } from 'react'

class Search extends Component {
    constructor () {
        super()

        this.onDeleteClick = this.onDeleteClick.bind(this)
        this.onEditClick = this.onEditClick.bind(this)
    }

    onEditClick = (key) => {
        if (this.props.onEditClick) {
            this.props.onEditClick(key)
        }
    }

    onDeleteClick = (key) => {
        if (this.props.onDeleteClick) {
            console.log('deleting...')
            this.props.onDeleteClick(key)
        }
    }

    render() {
        return (
            <div>
                <table className="table is-striped">
                    <thead>
                        <tr>
                            <th>Actions</th>
                            <th>Title</th>
                            <th>Min Players</th>
                            <th>Max Players</th>
                            <th>Added</th>
                        </tr>
                    </thead>
                    <tfoot>
                        <tr>
                            <th>Actions</th>
                            <th>Title</th>
                            <th>Min Players</th>
                            <th>Max Players</th>
                            <th>Added</th>
                        </tr>
                    </tfoot>
                    <tbody>
                        {this.props.data.map(elem => {
                            return <tr key={elem._key}>
                                <td>
                                <a className="button" onClick={this.onEditClick.bind(this, elem._key)}>
                                    <span className="icon is-small">
                                        <i className="fas fa-edit" title="edit"></i>
                                    </span>
                                </a>
                                <a className="button" onClick={this.onDeleteClick.bind(this, elem._key)}>
                                    <span className="icon is-small">
                                        <i className="fas fa-trash" title="delete"></i>
                                    </span>
                                </a>
                                </td>
                                <td>{elem.title}</td>
                                <td>{elem.minPlayers}</td>
                                <td>{elem.maxPlayers}</td>
                                <td>{elem.added}</td>
                            </tr>
                        })}
                    </tbody>
                </table>
            </div>)
    }
}

export default Search
