import { useState } from "react";
import PaidCheckbox from "./PaidCheckbox";
import axios from "axios";

interface ExpenseProps {
  expense: {
    id: number;
    title: string;
    cost: number;
    due: number;
  };
}

const Expense = ({ expense }: ExpenseProps) => {
  const [title, setTitle] = useState<string>(expense.title);
  const [cost, setCost] = useState<number>(expense.cost);
  const [due, setDue] = useState<number>(expense.due);
  const [isEditing, setIsEditing] = useState<boolean>(false);

  const handlePatch = async (payload: object) => {
    try {
      const res = await axios.patch(
        `http://localhost:8000/expenses/${expense.id}/`,
        payload
      );
      setTitle(res.data.title);
      setCost(res.data.cost);
      setDue(res.data.due);
    } catch (error) {
      console.error("Error updating expense:", error);
    }
  };

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleInputChange = (field: string, event: any) => {
    const { value } = event.target;
    const payload = { [field]: value };
    if (event.type === "blur" || event.key === "Enter") {
      handlePatch(payload);
      setIsEditing(false);
    } else {
      switch (field) {
        case "title":
          setTitle(value);
          break;
        case "cost":
          setCost(Number(value));
          break;
        case "due":
          setDue(Number(value));
          break;
        default:
          break;
      }
    }
  };

  const renderCell = (field: string, value: any) => {
    if (isEditing) {
      return (
        <input
          type="text"
          value={value}
          onChange={(event) => handleInputChange(field, event)}
          onBlur={(event) => handleInputChange(field, event)}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              event.preventDefault();
              handleInputChange(field, event);
            }
          }}
        />
      );
    } else {
      return <td onClick={() => handleEdit()}>{value}</td>;
    }
  };

  return (
    <table>
      <thead>
        <tr>
          <th>Título</th>
          <th>Custo</th>
          <th>Vencimento</th>
          <th>Pago?</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          {renderCell("title", title)}
          {renderCell("cost", cost)}
          {renderCell("due", due)}
          <td>
            <PaidCheckbox expense={expense} />
          </td>
        </tr>
      </tbody>
    </table>
  );
};

export default Expense;
