import React from 'react';
import { Route, Switch } from 'react-router-dom';
import Home from './components/Home';
import CredsForm from './components/SaveCreds';
import Navbar from './components/Navbar';

function App() {
    return (
        <main>
            <Switch>
		<Route path="/" component={Home} exact />
                <Route path="/creds" component={CredsForm} />
	        <Route component={Error} />
            </Switch>
	    <Navbar />
        </main>
    );
};
export default App;
