import { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

function GetGene() {
    const [form, setForm] = useState({
        gene: 'TP53',
        mutation: 'p.R175H',
        mutation_type: 'Missense',
    })

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null)
    const navigate = useNavigate();

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError(null)
        try {
            const res = await axios.post('http://localhost:5000/gene-fix', form)
            setLoading((prev) => !prev)
            navigate('/result', { state: res.data })
        } catch (err) {
            console.error(err)
            setError(err.response?.data?.error || 'Something went wrong!')
        }
    }

    return (
        <div className="max-w-lg mx-auto p-6">
            <h2 className="text-2xl font-semibold mb-4">🧬 GeneFixer - Enter Mutation Details</h2>

            {error && (
                <div className="mb-4 p-2 bg-red-100 text-red-700 rounded">
                    Error: {error}
                </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
                {/* Gene Name Dropdown */}
                <div>
                    <label htmlFor="gene" className="block font-medium">Gene Name:</label>
                    <select
                        name="gene"
                        id="gene"
                        value={form.gene}
                        onChange={handleChange}
                        className="w-full mt-1 border-gray-300 rounded-md shadow-sm"
                        required
                    >
                        <option value="TP53">TP53</option>
                        <option value="KRAS">KRAS</option>
                        <option value="EGFR">EGFR</option>
                        <option value="BRCA1">BRCA1</option>
                    </select>
                </div>

                {/* Mutation Dropdown */}
                <div>
                    <label htmlFor="mutation" className="block font-medium">Mutation (HGVS format):</label>
                    <select
                        name="mutation"
                        id="mutation"
                        value={form.mutation}
                        onChange={handleChange}
                        className="w-full mt-1 border-gray-300 rounded-md shadow-sm"
                        required
                    >
                        <option value="p.R175H">p.R175H</option>
                        <option value="p.G12D">p.G12D</option>
                        <option value="p.E746_A750del">p.E746_A750del</option>
                        <option value="p.C61G">p.C61G</option>
                    </select>
                </div>

                {/* Mutation Type Dropdown */}
                <div>
                    <label htmlFor="mutation_type" className="block font-medium">Mutation Type:</label>
                    <select
                        name="mutation_type"
                        id="mutation_type"
                        value={form.mutation_type}
                        onChange={handleChange}
                        className="w-full mt-1 border-gray-300 rounded-md shadow-sm"
                        required
                    >
                        <option value="Missense">Missense</option>
                        <option value="Nonsense">Nonsense</option>
                        <option value="Insertion">Insertion</option>
                        <option value="Deletion">Deletion</option>
                    </select>
                </div>

                {/* Submit Button */}
                <button
                    type="submit"
                    className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 flex items-center gap-2"
                    onClick={() => setLoading((prev) => !prev)}
                >
                    {loading ? (
                        <>
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="24" height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                className="lucide lucide-loader-circle animate-spin"
                            >
                                <path d="M21 12a9 9 0 1 1-6.219-8.56" />
                            </svg>
                            <h1>Analyzing ...</h1>
                        </>
                    ) : (
                        <>🧪 Analyze Mutation</>
                    )}
                </button>

            </form>
        </div>
    )
}

export default GetGene
