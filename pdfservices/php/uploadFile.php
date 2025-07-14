<?php

function uploadFileToFoxit($filePath, $clientId, $clientSecret, $host = 'https://na1.fusion.foxit.com') {
    // Check if file exists
    if (!file_exists($filePath)) {
        throw new Exception("File not found: $filePath");
    }
    
    // Prepare the upload URL
    $uploadUrl = $host . '/pdf-services/api/documents/upload';
    
    // Initialize cURL
    $ch = curl_init();
    
    // Create CURLFile object for the file
    $cFile = new CURLFile($filePath);
    
    // Prepare POST data
    $postData = array('file' => $cFile);
    
    // Set cURL options
    curl_setopt_array($ch, array(
        CURLOPT_URL => $uploadUrl,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $postData,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => array(
            'client_id: ' . $clientId,
            'client_secret: ' . $clientSecret
        ),
        CURLOPT_SSL_VERIFYPEER => true,
        CURLOPT_TIMEOUT => 300 // 5 minutes timeout
    ));
    
    // Execute the request
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    
    // Check for cURL errors
    if ($response === false) {
        $error = curl_error($ch);
        curl_close($ch);
        throw new Exception("cURL error: $error");
    }
    
    curl_close($ch);
    
    // Check HTTP status code
    if ($httpCode !== 200) {
        throw new Exception("HTTP error: $httpCode - $response");
    }
    
    // Parse JSON response
    $jsonResponse = json_decode($response, true);
    
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("Invalid JSON response: " . json_last_error_msg());
    }
    
    // Return the document ID
    return $jsonResponse['documentId'];
}

// Example usage
try {
    $clientId = 'your_client_id';
    $clientSecret = 'your_client_secret';
    $filePath = '/path/to/your/document.pdf';
    
    $documentId = uploadFileToFoxit($filePath, $clientId, $clientSecret);
    
    echo "File uploaded successfully! Document ID: $documentId\n";
    
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}

?>