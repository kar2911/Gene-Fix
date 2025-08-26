import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';
import 'highlight.js/styles/github.css'; // Or another theme

import React from 'react'

const MarkdownRenderer = ({content}) => {
  return (
    <div className="prose max-w-none">
    <ReactMarkdown
      children={content}
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeHighlight]}
    />
  </div>
  )
}

export default MarkdownRenderer
