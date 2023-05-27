import { useState } from "react";
import axios from "axios";

const PaidCheckbox = ({ expense }: any) => {
  const [paid, setPaid] = useState(expense.paid);

  const handleCheckboxChange = async () => {
    try {
      axios
        .patch(`http://localhost:8000/expenses/${expense.id}/payment/`)
        .then((res: any) => {
          setPaid(res.data.paid);
        });
    } catch (error) {
      console.error("Error updating payment:", error);
    }
  };

  return (
    <input type="checkbox" checked={paid} onChange={handleCheckboxChange} />
  );
};

export default PaidCheckbox;
