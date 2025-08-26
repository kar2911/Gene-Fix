import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import MarkdownRenderer from '../components/MarkdownRenderer';

const Live_Simulate = () => {
    const { state } = useLocation();
    const [resultData, setResultData] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!state) {
            navigate('/gene-fix');
            return;
        }

        const fetchLiveSimulation = async () => {
            try {
                const res = await fetch('http://localhost:8000/live-simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(state),
                });
                const data = await res.json();
                setResultData(data);
            } catch (err) {
                console.error('Error during live simulation fetch:', err);
            }
        };

        fetchLiveSimulation();
    }, [state]);

    if (!resultData) return <div className="p-6">Running live simulation...</div>;

    const { ai_response } = resultData;

    return (
        <div className="p-6 max-w-5xl mx-auto">
            <h1 className="text-3xl font-bold mb-6">Live Simulation Result</h1>

            <div>
                <MarkdownRenderer content={ai_response}/>
            </div>

            <div className="text-center mt-6">
                <button
                    onClick={() => navigate('/gene-fix')}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded"
                >
                    Back to Simulation
                </button>
            </div>
        </div>
    );
};

export default Live_Simulate;
