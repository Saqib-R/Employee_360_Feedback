import { API_URL } from '../../environments/environment';

const BASE_URL : string = API_URL;

// ENDPOINTS
export const endpoints = {
    VIEW_FEEDBACK_API: BASE_URL + "upload",
    VANILLA_SUMMARY_API: BASE_URL + "vanilla_summarize_feedback",
    EXP_SUMMARY_API: BASE_URL + "expectations_summarize",
    EXPORT_SUMMARY_API: BASE_URL + "upload_feedback",
    DOWNLOAD_SUMMARY_CSV_API: BASE_URL + "download_feedback",
    CUSTOM_SUMMARY_API: BASE_URL + "custom_summarize",
    EMP_SUMMARIZED_API: BASE_URL + "get_summarized_feedback",
    GET_FEEDBACKS_API: BASE_URL + "get_feedback_data",
    UPLOAD_EXPECTATIONS_API: BASE_URL + "uploadExpectationData",
    STORE_EXPECTATIONS_API: BASE_URL + "storeExpectationData",
    GET_ALL_COLLECTIONS_API: BASE_URL + "get_collections",
    SELECT_COLLECTION_API: BASE_URL + "select_collection",
    GET_HR_FEEDBACKS_API: BASE_URL + "get_hr_summarized_feedback",
    APPROVE_SUMMARY_API: BASE_URL + "approve_summary",
    PROMPT_RAG_API: BASE_URL + "promptExpec",
}

