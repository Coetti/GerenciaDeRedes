import "../styles/ResponseCard.css";
import Calculator from "../assets/images/calculator.png";
import Thermometer from "../assets/images/hot.png";
const ResponseCard = ({ data }) => {
  console.log("data", data);
  return (
    <div className="response-card-container">
      <div className="response-card-icon-container">
        <img
          src={data.questionType === "calculator" ? Calculator : Thermometer}
          alt="calculator"
        />
      </div>
      <div className="question-answer-container">
        <div className="question">
          <span className="question-text">{data.question}</span>
        </div>
        <div className="answer">
          <span className="answer-text">{data.answer}</span>
        </div>
      </div>
    </div>
  );
};

export default ResponseCard;
