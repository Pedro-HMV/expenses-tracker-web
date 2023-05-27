import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import PaidCheckbox from "./components/PaidCheckbox";
import Expense from "./components/Expense";

function App() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/users/").then((res: any) => {
      setUsers(res.data);
    });
  }, []);

  return (
    <>
      <div>
        <ul>
          {users.map((user: any) => (
            <>
              <h1>{user.username}</h1>
              <li style={{ color: "white", listStyle: "none" }}>
                {user.expenses.map((expense: any) => (
                  <>
                    <Expense expense={expense} />
                  </>
                ))}
              </li>
            </>
          ))}
        </ul>
      </div>
    </>
  );
}

export default App;
