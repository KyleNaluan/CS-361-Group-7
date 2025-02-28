import "./App.css";
import { useState } from "react";
import Login from "./components/Login";

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    return (
        <div>
            {isLoggedIn ? (
                <>
                    <h1>Real-Time Threat Intelligence</h1>
                    <p>Welcome to the dashboard!</p>
                </>
            ) : (
                <Login onLogin={() => setIsLoggedIn(true)} />
            )}
        </div>
    );
}

export default App;