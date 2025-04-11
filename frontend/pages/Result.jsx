// Result.jsx
import { useLocation, useNavigate } from 'react-router-dom'

const Result = () => {
    const { state } = useLocation()
    const navigate = useNavigate()

    if (!state) {
        return <div>No data available. <button onClick={() => navigate('/')}>Go Back</button></div>
    }

    const { gene, mutation, mut_type, repair, trials } = state

    return (
        <div className="p-6">
            <h2 className="text-2xl font-bold mb-2">Mutation Report: {gene} – {mutation}</h2>
            <h3 className="text-lg font-semibold mb-2">Mutation Type: {mut_type}</h3>

            <h4 className="font-bold mt-4">CRISPR Repair Plan:</h4>
            <pre className="bg-gray-100 p-2">{repair || 'No CRISPR repair plan available.'}</pre>

            <h4 className="font-bold mt-4">Clinical Trials:</h4>
            <ul className="list-disc list-inside space-y-2">
                {trials.map((t, i) => (
                    <li key={i} className="bg-gray-50 p-2 rounded shadow">
                        <p><strong>Condition:</strong> {t.Condition}</p>
                        <p><strong>Status:</strong> {t.Status}</p>
                        <p><strong>Title:</strong> {t["Study Title"]}</p>
                    </li>
                ))}
            </ul>

            <button onClick={() => navigate('/gene-fix')} className="mt-4 bg-green-500 text-white px-4 py-2 rounded">Try Another</button>
        </div>
    )
}

export default Result
