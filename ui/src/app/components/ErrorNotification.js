import React, { Component } from 'react'

class ErrorNotification extends Component {
    constructor() {
        super()

        this.onClose = this.onClose.bind(this)
    }

    onClose = () => {
        this.props.onClose()
    }

    render() {
        return (
            <div>
                <div class="notification is-danger">
                    <button class="delete" onClick={this.onClose}></button>
                    {this.props.message}
                </div>
            </div>)
    }
}

export default ErrorNotification
