import React, { Component } from 'react'

class Search extends Component {
    render() {
        return (
            <div>
                <table className="table is-striped">
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Added</th>
                        </tr>
                    </thead>
                    <tfoot>
                        <tr>
                            <th>Title</th>
                            <th>Added</th>
                        </tr>
                    </tfoot>
                    <tbody>
                        {this.props.data.map(elem => {
                            return <tr key={elem._key}>
                                <td>{elem.title}</td>
                                <td>{elem.added}</td>
                            </tr>
                        })}
                    </tbody>
                </table>
            </div>)
    }
}

export default Search
