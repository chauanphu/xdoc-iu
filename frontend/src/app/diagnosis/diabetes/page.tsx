"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface FormData {
  BMI: string | null;
  AGE: string | null;
  Urea: string | null;
  Cr: string | null;
  HbA1c: string | null;
  Chol: string | null;
  TG: string | null;
  HDL: string | null;
  LDL: string | null;
  VLDL: string | null;
}

interface ExplanationSection {
  title: string;
  items: Array<{
    label: string;
    value: string;
    shap?: string;
    status?: string;
    normalRange?: string;
  }>;
}

interface ExplanationData {
  patientInfo: ExplanationSection;
  bloodMarkers: ExplanationSection;
  lipidProfile: ExplanationSection;
  kidneyFunction: ExplanationSection;
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
  };
  recommendations: {
    title: string;
    items: Array<{
      category: string;
      suggestions: string[];
    }>;
  };
}

const initialFormData: FormData = {
  BMI: null,
  AGE: null,
  Urea: null,
  Cr: null,
  HbA1c: null,
  Chol: null,
  TG: null,
  HDL: null,
  LDL: null,
  VLDL: null,
};

export default function DiabetesPrediction() {
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [result, setResult] = useState<{
    prediction: string;
    trustScore: number;
    explanation: ExplanationData;
    apiResult: string;
  } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const processedData = Object.entries(formData).reduce<Record<string, number | null>>((acc, [key, value]) => ({
        ...acc,
        [key]: value ? parseFloat(value) : null
      }), {});

      const response = await fetch("/api/diagnosis/predict/diabetes", {
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

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>, field: keyof FormData) => {
    const value = e.target.value === "" ? null : e.target.value;
    setFormData({ ...formData, [field]: value });
  };

  const renderMetricCard = (section: ExplanationSection) => (
    <Card className="mb-4 bg-gray-800/50 backdrop-blur border border-gray-700/50">
      <CardHeader>
        <CardTitle className="text-[#00BFFF]">{section.title}</CardTitle>
      </CardHeader>
      <CardContent className="text-gray-200">
        <div className="space-y-2">
          {section.items.map((item, index) => (
            <div key={index} className="flex justify-between items-center">
              <span className="font-medium">{item.label}:</span>
              <div className="text-right">
                <span className={`${
                  item.status === 'high' ? 'text-red-400 font-medium' :
                  item.status === 'low' ? 'text-yellow-400 font-medium' :
                  'text-emerald-400 font-medium'
                }`}>
                  {item.value}
                </span>
                {item.normalRange && (
                  <div className="text-sm text-gray-400">
                    Khoảng bình thường: {item.normalRange}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-700 via-gray-600 to-gray-900 p-8">
      <div className="container mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-[#00BFFF] to-blue-500">
          Đánh Giá Nguy Cơ Tiểu Đường
        </h1>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="bg-gray-800/50 backdrop-blur border border-gray-700/50">
            <CardHeader>
              <CardTitle className="text-[#00BFFF]">Thông Tin Bệnh Nhân</CardTitle>
              <CardDescription className="text-gray-300">
                Vui lòng nhập các chỉ số từ xét nghiệm máu gần nhất của bạn. Để có kết quả chính xác nhất, hãy đảm bảo nhập đúng các giá trị từ phiếu xét nghiệm.
              </CardDescription>
            </CardHeader>
            <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="age" className="flex items-center gap-1">
                    Tuổi
                    <span className="text-xs text-gray-400" title="Độ tuổi của bạn (từ 18-100 tuổi)">[?]</span>
                  </Label>
                  <Input
                    id="age"
                    type="number"
                    value={formData.AGE ?? ""}
                    onChange={(e) => handleInputChange(e, "AGE")}
                    placeholder="VD: 45"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="bmi" className="flex items-center gap-1">
                    Chỉ số BMI
                    <span className="text-xs text-gray-400" title="Chỉ số khối cơ thể (kg/m²). Mức bình thường: 18.5-24.9">[?]</span>
                  </Label>
                  <Input
                    id="bmi"
                    type="number"
                    step="0.1"
                    value={formData.BMI ?? ""}
                    onChange={(e) => handleInputChange(e, "BMI")}
                    placeholder="VD: 23.5"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="hba1c" className="flex items-center gap-1">
                    HbA1c (%)
                    <span className="text-xs text-gray-400" title="Chỉ số đường huyết trung bình trong 2-3 tháng qua. Bình thường: 4-5.6%">[?]</span>
                  </Label>
                  <Input
                    id="hba1c"
                    type="number"
                    step="0.1"
                    value={formData.HbA1c ?? ""}
                    onChange={(e) => handleInputChange(e, "HbA1c")}
                    placeholder="VD: 5.2"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="chol" className="flex items-center gap-1">
                    Cholesterol
                    <span className="text-xs text-gray-400" title="Cholesterol tổng trong máu (mg/dL). Mức bình thường: dưới 200 mg/dL">[?]</span>
                  </Label>
                  <Input
                    id="chol"
                    type="number"
                    value={formData.Chol ?? ""}
                    onChange={(e) => handleInputChange(e, "Chol")}
                    placeholder="VD: 180"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="tg" className="flex items-center gap-1">
                    Triglycerides
                    <span className="text-xs text-gray-400" title="Lượng mỡ trong máu (mg/dL). Mức bình thường: dưới 150 mg/dL">[?]</span>
                  </Label>
                  <Input
                    id="tg"
                    type="number"
                    value={formData.TG ?? ""}
                    onChange={(e) => handleInputChange(e, "TG")}
                    placeholder="VD: 140"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="hdl" className="flex items-center gap-1">
                    HDL
                    <span className="text-xs text-gray-400" title="Cholesterol có lợi (mg/dL). Mức bình thường: trên 40 mg/dL (nam), trên 50 mg/dL (nữ)">[?]</span>
                  </Label>
                  <Input
                    id="hdl"
                    type="number"
                    value={formData.HDL ?? ""}
                    onChange={(e) => handleInputChange(e, "HDL")}
                    placeholder="VD: 45"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="ldl" className="flex items-center gap-1">
                    LDL
                    <span className="text-xs text-gray-400" title="Cholesterol có hại (mg/dL). Mức bình thường: dưới 100 mg/dL">[?]</span>
                  </Label>
                  <Input
                    id="ldl"
                    type="number"
                    value={formData.LDL ?? ""}
                    onChange={(e) => handleInputChange(e, "LDL")}
                    placeholder="VD: 90"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="vldl" className="flex items-center gap-1">
                    VLDL
                    <span className="text-xs text-gray-400" title="Lipoprotein mật độ rất thấp (mg/dL). Mức bình thường: 2-30 mg/dL">[?]</span>
                  </Label>
                  <Input
                    id="vldl"
                    type="number"
                    value={formData.VLDL ?? ""}
                    onChange={(e) => handleInputChange(e, "VLDL")}
                    placeholder="VD: 25"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="urea" className="flex items-center gap-1">
                    Ure
                    <span className="text-xs text-gray-400" title="Nồng độ ure trong máu (mg/dL). Mức bình thường: 15-40 mg/dL">[?]</span>
                  </Label>
                  <Input
                    id="urea"
                    type="number"
                    value={formData.Urea ?? ""}
                    onChange={(e) => handleInputChange(e, "Urea")}
                    placeholder="VD: 30"
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="cr" className="flex items-center gap-1">
                    Creatinine
                    <span className="text-xs text-gray-400" title="Chỉ số đánh giá chức năng thận (mg/dL). Mức bình thường: 0.7-1.2 mg/dL (nam), 0.5-1.0 mg/dL (nữ)">[?]</span>
                  </Label>
                  <Input
                    id="cr"
                    type="number"
                    step="0.1"
                    value={formData.Cr ?? ""}
                    onChange={(e) => handleInputChange(e, "Cr")}
                    placeholder="VD: 0.9"
                  />
                </div>
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

            {result.explanation.bloodMarkers && renderMetricCard(result.explanation.bloodMarkers)}
            {result.explanation.lipidProfile && renderMetricCard(result.explanation.lipidProfile)}
            {result.explanation.kidneyFunction && renderMetricCard(result.explanation.kidneyFunction)}

            {result.explanation.analysis && (
              <Card className="bg-gray-800/50 backdrop-blur border border-gray-700/50">
                <CardHeader>
                  <CardTitle className="text-[#00BFFF]">{result.explanation.analysis.title}</CardTitle>
                </CardHeader>
                <CardContent className="text-gray-200">
                  <div className="space-y-4">
                    {result.explanation.analysis.mainFactors.map((factor, index) => (
                      <div key={index} className="border-b border-gray-700/50 pb-2 last:border-0">
                        <h4 className="font-medium text-gray-200">{factor.factor}</h4>
                        <p className="text-sm text-gray-300">{factor.explanation}</p>
                        <span className={`text-sm font-medium ${
                          factor.impact === 'high' ? 'text-red-400' :
                          factor.impact === 'medium' ? 'text-yellow-400' :
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

            {result.explanation.recommendations && (
              <Card className="bg-gray-800/50 backdrop-blur border border-gray-700/50">
                <CardHeader>
                  <CardTitle className="text-[#00BFFF]">{result.explanation.recommendations.title}</CardTitle>
                </CardHeader>
                <CardContent className="text-gray-200">
                  <div className="space-y-4">
                    {result.explanation.recommendations.items.map((item, index) => (
                      <div key={index}>
                        <h4 className="font-medium mb-2 text-[#00BFFF]">{item.category}</h4>
                        <ul className="list-disc list-inside space-y-1 text-gray-300">
                          {item.suggestions.map((suggestion, sIndex) => (
                            <li key={sIndex} className="text-sm text-gray-300">{suggestion}</li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        )}
       </div>
     </div>
   </main>
 );
}