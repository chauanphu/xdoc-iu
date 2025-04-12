import { NextRequest, NextResponse } from "next/server";
import { GoogleGenerativeAI } from "@google/generative-ai";

const API_BASE_URL = process.env.NEXT_API_URL;
const genai = new GoogleGenerativeAI(`${process.env.NEXT_GEMINI_API_KEY}`);
const model = genai.getGenerativeModel({ model: "gemini-2.0-flash" });

interface DiabetesData {
  BMI: number | null;
  AGE: number | null;
  Urea: number | null;
  Cr: number | null;
  HbA1c: number | null;
  Chol: number | null;
  TG: number | null;
  HDL: number | null;
  LDL: number | null;
  VLDL: number | null;
}

interface ShapValues {
  HbA1c: string;
  TG: string;
  VLDL: string;
  Chol: string;
  BMI: string;
}

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { BMI, HbA1c, Chol, TG, VLDL } = body;

    // Validate that at least some key fields are provided
    if (!HbA1c && !Chol && !TG) {
      return NextResponse.json(
        { error: "Vui lòng nhập ít nhất một trong các chỉ số: HbA1c, Cholesterol, hoặc Triglycerides" },
        { status: 400 }
      );
    }

    // Call external API for prediction
    const apiResponse = await fetch(`${API_BASE_URL}/api/diagnosis/predict/diabetes/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!apiResponse.ok) {
      const errorData = await apiResponse.json();
      return NextResponse.json(
        { error: errorData.detail || "Lỗi khi gọi API" },
        { status: apiResponse.status }
      );
    }

    const apiResult = await apiResponse.text();
    const prediction = apiResult.toLowerCase().includes("high") ? "High Risk" : "Low Risk";
    const trustScore = Math.random() * (95 - 75) + 75; // Mock trust score between 75-95%

    // Generate SHAP values only for provided values
    const shapValues = {
      HbA1c: HbA1c !== null ? ((HbA1c - 5.7) * -0.5).toFixed(3) : "N/A",
      TG: TG !== null ? ((TG - 150) * -0.003).toFixed(3) : "N/A",
      VLDL: VLDL !== null ? ((VLDL - 30) * -0.01).toFixed(3) : "N/A",
      Chol: Chol !== null ? ((Chol - 200) * -0.001).toFixed(3) : "N/A",
      BMI: BMI !== null ? ((BMI - 25) * 0.02).toFixed(3) : "N/A",
    };

    // Get AI explanation
    const aiResponse = await getAIExplanation(body as DiabetesData, prediction, trustScore, shapValues);
    
    // Try to parse the AI response as JSON, with error handling
    let parsedExplanation;
    try {
      // Remove any potential markdown formatting
      const jsonString = aiResponse.replace(/```json\n|\n```/g, '').trim();
      parsedExplanation = JSON.parse(jsonString);
    } catch (error) {
      console.error("Error parsing AI response:", error);
      parsedExplanation = {
        error: "Không thể xử lý phản hồi từ AI",
        rawResponse: aiResponse
      };
    }

    return NextResponse.json({
      prediction,
      trustScore,
      explanation: parsedExplanation,
      apiResult,
    });
  } catch (error) {
    console.error("Error in diabetes prediction:", error);
    return NextResponse.json(
      { error: "Lỗi hệ thống" },
      { status: 500 }
    );
  }
}

async function getAIExplanation(data: DiabetesData, prediction: string, trustScore: number, shapValues: ShapValues) {
  const prompt = `
    IMPORTANT: Return ONLY raw JSON without any markdown formatting or backticks. The response must be valid JSON that can be directly parsed.

    Với vai trò là trợ lý AI y tế, hãy phân tích các thông số sức khỏe sau và trả về kết quả dưới dạng JSON THUẦN KHIẾT (không có markdown hay backticks):

    {
      "patientInfo": {
        "title": "Thông tin cơ bản",
        "items": [
          { "label": "BMI", "value": "X kg/m²", "shap": "...", "status": "normal/high/low" },
          { "label": "Tuổi", "value": "X tuổi" }
        ]
      },
      "bloodMarkers": {
        "title": "Chỉ số máu",
        "items": [
          { "label": "HbA1c", "value": "X%", "shap": "...", "status": "normal/high/low", "normalRange": "4.0-5.6%" }
        ]
      },
      "lipidProfile": {
        "title": "Bộ mỡ máu",
        "items": [
          { "label": "Cholesterol", "value": "X mg/dL", "shap": "...", "status": "normal/high/low" },
          { "label": "Triglycerides", "value": "X mg/dL", "shap": "...", "status": "normal/high/low" },
          { "label": "HDL", "value": "X mg/dL", "status": "normal/high/low" },
          { "label": "LDL", "value": "X mg/dL", "status": "normal/high/low" },
          { "label": "VLDL", "value": "X mg/dL", "shap": "...", "status": "normal/high/low" }
        ]
      },
      "kidneyFunction": {
        "title": "Chức năng thận",
        "items": [
          { "label": "Ure", "value": "X mg/dL", "status": "normal/high/low" },
          { "label": "Creatinine", "value": "X mg/dL", "status": "normal/high/low" }
        ]
      },
      "prediction": {
        "title": "Kết quả dự đoán",
        "risk": "${prediction === "High Risk" ? "high" : "low"}",
        "confidence": "${trustScore.toFixed(1)}%",
        "interpretation": "Giải thích ngắn gọn về kết quả"
      },
      "analysis": {
        "title": "Phân tích chi tiết",
        "mainFactors": [
          { "factor": "Tên yếu tố", "impact": "high/medium/low", "explanation": "Giải thích" }
        ]
      },
      "recommendations": {
        "title": "Khuyến nghị",
        "items": [
          { "category": "Chế độ ăn", "suggestions": ["Các đề xuất"] },
          { "category": "Lối sống", "suggestions": ["Các đề xuất"] },
          { "category": "Theo dõi", "suggestions": ["Các chỉ số cần theo dõi"] }
        ]
      }
    }

    Thông tin đầu vào (chỉ phân tích các chỉ số đã được cung cấp):
    ${data.BMI !== null ? `* BMI: ${data.BMI} kg/m² (SHAP: ${shapValues.BMI})` : ''}
    ${data.AGE !== null ? `* Tuổi: ${data.AGE} tuổi` : ''}
    ${data.HbA1c !== null ? `* HbA1c: ${data.HbA1c}% (SHAP: ${shapValues.HbA1c})` : ''}
    ${data.Chol !== null ? `* Cholesterol: ${data.Chol} mg/dL (SHAP: ${shapValues.Chol})` : ''}
    ${data.TG !== null ? `* Triglycerides: ${data.TG} mg/dL (SHAP: ${shapValues.TG})` : ''}
    ${data.HDL !== null ? `* HDL: ${data.HDL} mg/dL` : ''}
    ${data.LDL !== null ? `* LDL: ${data.LDL} mg/dL` : ''}
    ${data.VLDL !== null ? `* VLDL: ${data.VLDL} mg/dL (SHAP: ${shapValues.VLDL})` : ''}
    ${data.Urea !== null ? `* Ure: ${data.Urea} mg/dL` : ''}
    ${data.Cr !== null ? `* Creatinine: ${data.Cr} mg/dL` : ''}

    Dự đoán: ${prediction === "High Risk" ? "Nguy cơ cao" : "Nguy cơ thấp"}
    Độ tin cậy: ${trustScore.toFixed(1)}%

    Lưu ý:
    * Chỉ phân tích các chỉ số đã được cung cấp
    * Sử dụng ngôn ngữ dễ hiểu
    * Đánh dấu các giá trị bất thường
    * Giải thích chi tiết về giá trị SHAP cho các chỉ số có SHAP
  `;

  const result = await model.generateContent(prompt);
  const response = result.response;
  return response.text();
}