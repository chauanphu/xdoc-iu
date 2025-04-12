"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface FormData {
  age: string | null;
  gender: string | null;
  blood_pressure: string | null;
  cholesterol_level: string | null;
  exercise_habits: string | null;
  smoking: string | null;
  family_heart_disease: string | null;
  diabetes: string | null;
  bmi: string | null;
  high_blood_pressure: string | null;
  low_hdl_cholesterol: string | null;
  high_ldl_cholesterol: string | null;
  alcohol_consumption: string | null;
  stress_level: string | null;
  sleep_hours: string | null;
  sugar_consumption: string | null;
  triglyceride_level: string | null;
  fasting_blood_sugar: string | null;
  crp_level: string | null;
  homocysteine_level: string | null;
}

interface ExplanationSection {
  title: string;
  items: Array<{
    label: string;
    value: string;
    shap?: string;
    status?: string;
    impact?: string;
  }>;
}

interface RiskFactor {
  category: string;
  factors: string[];
}

interface ExplanationData {
  patientInfo: ExplanationSection;
  vitals: ExplanationSection;
  lifestyle: ExplanationSection;
  biomarkers: ExplanationSection;
  prediction: {
    title: string;
    risk: string;
    confidence: string;
    interpretation: string;
  };
  analysis: {
    title: string;
    mainFactors: Array<{
      factor: string;
      impact: string;
      explanation: string;
    }>;
    riskFactors: RiskFactor[];
  };
  recommendations: {
    title: string;
    lifestyle: string[];
    monitoring: string[];
    prevention: string[];
  };
}

const initialFormData: FormData = {
  age: null,
  gender: "Male",
  blood_pressure: null,
  cholesterol_level: null,
  exercise_habits: "Low",
  smoking: "No",
  family_heart_disease: "No", 
  diabetes: "No",
  bmi: null,
  high_blood_pressure: "No",
  low_hdl_cholesterol: "No",
  high_ldl_cholesterol: "No",
  alcohol_consumption: "Low",
  stress_level: "No",
  sleep_hours: null,
  sugar_consumption: "Low",
  triglyceride_level: null,
  fasting_blood_sugar: null,
  crp_level: null,
  homocysteine_level: null
};

export default function CardiovascularPrediction() {
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [result, setResult] = useState<{
    prediction: string;
    trustScore: number;
    explanation: ExplanationData;
    apiResult: string;
  } | null>(null);

  // Helper function for consistent form field rendering
  const renderFormField = (
    label: string,
    id: keyof FormData,
    type: "number" | "select",
    options?: { value: string; label: string }[],
    tooltip?: string
  ) => (
    <div className="space-y-2">
      <Label htmlFor={id} className="flex items-center gap-1">
        {label}
        {tooltip && <span className="text-xs text-gray-400" title={tooltip}>[?]</span>}
      </Label>
      {type === "select" && options ? (
        <select
          id={id}
          className="w-full p-2 border rounded bg-gray-700/50 border-gray-600 text-gray-200"
          value={formData[id] ?? ""}
          onChange={(e) => handleInputChange(e, id)}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      ) : (
        <Input
          id={id}
          type="number"
          step={id === "bmi" || id === "crp_level" || id === "homocysteine_level" ? "0.1" : undefined}
          value={formData[id] ?? ""}
          onChange={(e) => handleInputChange(e, id)}
        />
      )}
    </div>
  );


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const processedData = {
        ...formData,
        age: formData.age ? parseInt(formData.age) : null,
        blood_pressure: formData.blood_pressure ? parseInt(formData.blood_pressure) : null,
        cholesterol_level: formData.cholesterol_level ? parseInt(formData.cholesterol_level) : null,
        bmi: formData.bmi ? parseFloat(formData.bmi) : null,
        sleep_hours: formData.sleep_hours ? parseInt(formData.sleep_hours) : null,
        triglyceride_level: formData.triglyceride_level ? parseInt(formData.triglyceride_level) : null,
        fasting_blood_sugar: formData.fasting_blood_sugar ? parseInt(formData.fasting_blood_sugar) : null,
        crp_level: formData.crp_level ? parseFloat(formData.crp_level) : null,
        homocysteine_level: formData.homocysteine_level ? parseFloat(formData.homocysteine_level) : null,
      };

      const response = await fetch("/api/diagnosis/predict/cardiovascular", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(processedData),
      });

      const data = await response.json();

      if ('error' in data) {
        setError(typeof data.error === 'string' ? data.error : 'Lỗi không xác định');
        setResult(null);
      } else if (!data.explanation || !data.prediction) {
        setError("Lỗi khi xử lý kết quả phân tích");
        setResult(null);
      } else {
        setResult(data);
        setError(null);
      }
    } catch (error) {
      console.error("Error:", error);
      setError(error instanceof Error ? error.message : "Có lỗi xảy ra khi gửi yêu cầu");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
    field: keyof FormData
  ) => {
    const value = e.target.value === "" ? null : e.target.value;
    setFormData({ ...formData, [field]: value });
  };

  const renderMetricCard = (section: ExplanationSection) => (
    <Card className="mb-4 bg-gray-800/50 backdrop-blur border border-gray-700/50">
      <CardHeader>
        <CardTitle className="text-[#00BFFF]">{section.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {section.items.map((item, index) => (
            <div key={index} className="flex justify-between items-center text-gray-200">
              <span className="font-medium">{item.label}:</span>
              <div className="text-right">
                <span className={`${
                  item.status === 'high' ? 'text-red-400 font-medium' :
                  item.status === 'low' ? 'text-yellow-400 font-medium' :
                  'text-emerald-400 font-medium'
                } text-base`}>
                  {item.value}
                </span>
                <div className="text-sm">
                  {item.impact && (
                    <span className={`${
                      item.impact === 'high' ? 'text-red-400' :
                      item.impact === 'medium' ? 'text-yellow-400' :
                      'text-[#00BFFF]'
                    } font-medium`}>
                      Mức độ: {
                        item.impact === 'high' ? 'Cao' :
                        item.impact === 'medium' ? 'Trung bình' :
                        'Thấp'
                      }
                    </span>
                  )}
                </div>
                {item.shap && (
                  <div className="text-sm text-gray-400">
                    SHAP: {item.shap}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );

  const renderRiskFactors = (riskFactors: RiskFactor[]) => (
    <div className="space-y-4">
      {riskFactors.map((category, index) => (
        <div key={index}>
          <h4 className="font-medium mb-2 text-gray-200">{category.category}</h4>
          <ul className="list-disc list-inside space-y-1">
            {category.factors.map((factor, fIndex) => (
              <li key={fIndex} className="text-sm text-gray-300">{factor}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );

  const renderRecommendations = (recommendations: ExplanationData['recommendations']) => (
    <Card className="bg-gray-800/50 backdrop-blur border border-gray-700/50">
      <CardHeader>
        <CardTitle className="text-[#00BFFF]">{recommendations.title}</CardTitle>
      </CardHeader>
      <CardContent className="text-gray-200">
        <div className="space-y-4">
          <div>
            <h4 className="font-medium mb-2">Lối sống</h4>
            <ul className="list-disc list-inside space-y-1 text-gray-300">
              {recommendations.lifestyle.map((item, index) => (
                <li key={index} className="text-sm">{item}</li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="font-medium mb-2">Theo dõi</h4>
            <ul className="list-disc list-inside space-y-1 text-gray-300">
              {recommendations.monitoring.map((item, index) => (
                <li key={index} className="text-sm">{item}</li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="font-medium mb-2">Phòng ngừa</h4>
            <ul className="list-disc list-inside space-y-1 text-gray-300">
              {recommendations.prevention.map((item, index) => (
                <li key={index} className="text-sm">{item}</li>
              ))}
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>
  );
  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-700 via-gray-600 to-gray-900 p-8">
      <div className="container mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-[#00BFFF] to-blue-500">
          Đánh Giá Nguy Cơ Tim Mạch
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-gray-800/50 backdrop-blur border border-gray-700/50">
          <CardHeader>
            <CardTitle className="text-[#00BFFF]">Thông Tin Bệnh Nhân</CardTitle>
            <CardDescription className="text-gray-300">
              Vui lòng điền đầy đủ thông tin sức khỏe của bạn. Các chỉ số càng chính xác, kết quả dự đoán càng đáng tin cậy. Đối với các chỉ số xét nghiệm, hãy sử dụng kết quả gần nhất của bạn.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Basic Information */}
                {renderFormField("Tuổi", "age", "number", undefined, "Độ tuổi của bạn (từ 18-100 tuổi)")}
                {renderFormField("Giới tính", "gender", "select", [
                  { value: "Male", label: "Nam" },
                  { value: "Female", label: "Nữ" }
                ])}
                {renderFormField("Huyết áp", "blood_pressure", "number", undefined, "Huyết áp tâm thu (mmHg). Mức bình thường: 90-120 mmHg")}
                {renderFormField("Cholesterol", "cholesterol_level", "number", undefined, "Cholesterol tổng trong máu (mg/dL). Mức bình thường: dưới 200 mg/dL")}
                {renderFormField("Chỉ số BMI", "bmi", "number", undefined, "Chỉ số khối cơ thể (kg/m²). Mức bình thường: 18.5-24.9")}

                {/* Lifestyle */}
                {renderFormField("Tập thể dục", "exercise_habits", "select", [
                  { value: "Low", label: "Ít" },
                  { value: "Medium", label: "Trung bình" },
                  { value: "High", label: "Nhiều" }
                ], "Mức độ vận động thể chất: Ít (dưới 1h/tuần), Trung bình (1-3h/tuần), Nhiều (trên 3h/tuần)")}
                {renderFormField("Hút thuốc", "smoking", "select", [
                  { value: "No", label: "Không" },
                  { value: "Yes", label: "Có" }
                ], "Thói quen hút thuốc lá hiện tại hoặc trong 5 năm gần đây")}
                {renderFormField("Tiền sử tim mạch gia đình", "family_heart_disease", "select", [
                  { value: "No", label: "Không" },
                  { value: "Yes", label: "Có" }
                ], "Gia đình có người thân (cha, mẹ, anh chị em ruột) mắc bệnh tim mạch trước 55 tuổi")}
                {renderFormField("Tiểu đường", "diabetes", "select", [
                  { value: "No", label: "Không" },
                  { value: "Yes", label: "Có" }
                ], "Bạn đã được chẩn đoán mắc bệnh tiểu đường type 1 hoặc type 2")}
                {renderFormField("Số giờ ngủ", "sleep_hours", "number", undefined, "Số giờ ngủ trung bình mỗi ngày. Mức khuyến nghị: 7-9 giờ/ngày")}
                {renderFormField("Mức độ stress", "stress_level", "select", [
                  { value: "No", label: "Thấp" },
                  { value: "Yes", label: "Cao" }
                ], "Đánh giá mức độ căng thẳng trong cuộc sống hàng ngày của bạn")}

                {/* Consumption */}
                {renderFormField("Tiêu thụ đường", "sugar_consumption", "select", [
                  { value: "Low", label: "Ít" },
                  { value: "Medium", label: "Trung bình" },
                  { value: "High", label: "Nhiều" }
                ], "Mức độ tiêu thụ đường: Ít (< 25g/ngày), Trung bình (25-50g/ngày), Nhiều (> 50g/ngày)")}
                {renderFormField("Tiêu thụ rượu bia", "alcohol_consumption", "select", [
                  { value: "Low", label: "Ít" },
                  { value: "Medium", label: "Trung bình" },
                  { value: "High", label: "Nhiều" }
                ], "Mức độ tiêu thụ rượu bia: Ít (< 1 ly/ngày), Trung bình (1-2 ly/ngày), Nhiều (> 2 ly/ngày)")}

                {/* Medical Metrics */}
                {renderFormField("Triglycerides", "triglyceride_level", "number", undefined, "Lượng mỡ trong máu (mg/dL). Mức bình thường: dưới 150 mg/dL")}
                {renderFormField("Đường huyết lúc đói", "fasting_blood_sugar", "number", undefined, "Nồng độ đường trong máu khi đói (mg/dL). Mức bình thường: 70-100 mg/dL")}
                {renderFormField("CRP", "crp_level", "number", undefined, "Protein phản ứng C (mg/L). Mức bình thường: dưới 3 mg/L")}
                {renderFormField("Homocysteine", "homocysteine_level", "number", undefined, "Amino acid trong máu (µmol/L). Mức bình thường: 5-15 µmol/L")}
              </div>
              <Button
                type="submit"
                className="w-full bg-[#00BFFF] hover:bg-[#00BFFF]/80 text-white transition-colors"
                disabled={loading}
              >
                {loading ? "Đang phân tích..." : "Phân Tích Nguy Cơ"}
              </Button>
            </form>
          </CardContent>
        </Card>

        {error && typeof error === 'string' && (
          <Card className="bg-gray-800/50 backdrop-blur border border-gray-700/50">
            <CardHeader>
              <CardTitle className="text-[#00BFFF]">Lỗi</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-red-500">{error}</p>
            </CardContent>
          </Card>
        )}

        {result && result.explanation && (
          <div className="space-y-6">
            <Card className="bg-gray-800/50 backdrop-blur border border-gray-700/50">
              <CardHeader>
                <CardTitle className="text-[#00BFFF]">{result.explanation.prediction.title}</CardTitle>
                <CardDescription className="text-gray-300">
                  Mức độ nguy cơ:{" "}
                  <span className={result.explanation.prediction.risk === "high" ? "text-red-500" : "text-green-500"}>
                    {result.explanation.prediction.risk === "high" ? "Nguy Cơ Cao" : "Nguy Cơ Thấp"}
                  </span>
                </CardDescription>
              </CardHeader>
              <CardContent>
                {result.trustScore && (
                  <div className="mb-4">
                    <h3 className={`font-semibold mb-2 ${result.trustScore > 50 ? 'text-green-300' : 'text-red-300'}`}>Độ Tin Cậy</h3>
                    <div className="w-full bg-gray-700/50 rounded-full h-4">
                      <div
                        className="h-4 rounded-full bg-[#00BFFF]"
                        style={{ width: `${result.trustScore}%` }}
                      />
                    </div>
                    <p className="text-sm text-gray-300 mt-1">
                      {result.trustScore.toFixed(1)}% độ tin cậy
                    </p>
                  </div>
                )}
                <p className="text-sm text-gray-300">
                  {result.explanation.prediction.interpretation}
                </p>
              </CardContent>
            </Card>

            {result.explanation.vitals && renderMetricCard(result.explanation.vitals)}
            {result.explanation.biomarkers && renderMetricCard(result.explanation.biomarkers)}
            
            {result.explanation.analysis && (
              <Card className="bg-gray-800/50 backdrop-blur border border-gray-700/50">
                <CardHeader>
                  <CardTitle className="text-[#00BFFF]">{result.explanation.analysis.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {result.explanation.analysis.mainFactors.map((factor, index) => (
                      <div key={index} className="border-b border-gray-600/50 pb-2 last:border-0">
                        <h4 className="font-medium text-gray-200">{factor.factor}</h4>
                        <p className="text-sm text-gray-300">{factor.explanation}</p>
                        <span className={`text-sm ${
                          factor.impact === 'high' ? 'text-red-500' :
                          factor.impact === 'medium' ? 'text-yellow-500' :
                          'text-blue-500'
                        }`}>
                          Mức độ ảnh hưởng: {
                            factor.impact === 'high' ? 'Cao' :
                            factor.impact === 'medium' ? 'Trung bình' :
                            'Thấp'
                          }
                        </span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {result.explanation.analysis && result.explanation.analysis.riskFactors && (
              <Card className="bg-gray-800/50 backdrop-blur border border-gray-700/50">
                <CardHeader>
                  <CardTitle className="text-[#00BFFF]">Yếu tố nguy cơ</CardTitle>
                </CardHeader>
                <CardContent>
                  {renderRiskFactors(result.explanation.analysis.riskFactors)}
                </CardContent>
              </Card>
            )}

            {result.explanation.recommendations && renderRecommendations(result.explanation.recommendations)}
          </div>
        )}
        </div>
      </div>
    </main>
  );
}