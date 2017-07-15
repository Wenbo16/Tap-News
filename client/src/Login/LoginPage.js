import React, {PropTypes} from 'react';
import Auth from '../Auth/Auth';
import LoginForm from './LoginForm';

class LoginPage extends React.Component {
    constructor(props, context) {
        super(props, context);

        this.state = {
            errors: {
                // summary : 'Summary Error',
                // email : 'Email Error',
                // password: 'Password Error'
            },

            user: {
                email: '',
                password: ''
            }
        };
    }

    onSubmit(event) {
        event.preventDefault();

        const email = this.state.user.email;
        const password = this.state.user.password;

        console.log('email:' + email);
        console.log('password:' + password);

        // Post login data and handle response.
        fetch('http://localhost:3000/auth/login', {
            method: 'POST',
            cache: false,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            // A body is an instance of any of the following types:
            body: JSON.stringify({
                email: this.state.user.email,
                password: this.state.user.password
            })
        }).then(response => {
            if (response.status === 200) {
                this.setState({
                  errors: {}
                });

                // The Body mixin defines the following methods to extract a body (implemented by both Request and Response). 
                // These all return a promise that is eventually resolved with the actual content.
                response.json().then(function(json) {
                    Auth.authenticateUser(json.token, email);
                    this.context.router.replace('/');
                }.bind(this));
            } else {
                console.log('Login failed');
                response.json().then(function(json) {
                    const errors = json.errors ? json.errors : {};
                    errors.summary = json.message;
                    this.setState({errors});
                }.bind(this));
            }
        });
    }

    changeUser(event) {
        console.log('input changed');
        const field = event.target.name;
        const user = this.state.user;
        user[field] = event.target.value;
        this.setState({
            user
        });
    }

    render() {
        return (
          <LoginForm
            onSubmit={this.onSubmit.bind(this)}
            onChange={this.changeUser.bind(this)}
            errors={this.state.errors}
          />
        );
    }
}

// To make react-router work
LoginPage.contextTypes = {
    router: PropTypes.object.isRequired
};

export default LoginPage;