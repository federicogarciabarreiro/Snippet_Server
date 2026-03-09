// Portfolio sample: Unity WebGL API client with coroutines and no third-party SDKs.

using System;
using System.Collections;
using System.Text;
using UnityEngine;
using UnityEngine.Networking;

public class PortfolioServerApi : MonoBehaviour
{
    public string BaseUrl;
    public string Token;

    public IEnumerator Login(string email, string password, Action<string> onSuccess, Action<string> onError)
    {
        WWWForm form = new WWWForm();
        form.AddField("username", email);
        form.AddField("password", password);

        using (UnityWebRequest req = UnityWebRequest.Post(BaseUrl + "/api/v1/auth/login", form))
        {
            yield return req.SendWebRequest();
            if (req.result != UnityWebRequest.Result.Success)
            {
                onError?.Invoke(req.error);
                yield break;
            }

            onSuccess?.Invoke(req.downloadHandler.text);
        }
    }

    public IEnumerator UnitySessionStart(string jsonPayload, Action<string> onSuccess, Action<string> onError)
    {
        yield return SendJson("/api/v1/commerce/unity/sessions/start", "POST", jsonPayload, onSuccess, onError);
    }

    public IEnumerator UnitySessionEvent(string sessionId, string jsonPayload, Action<string> onSuccess, Action<string> onError)
    {
        yield return SendJson($"/api/v1/commerce/unity/sessions/{sessionId}/events", "POST", jsonPayload, onSuccess, onError);
    }

    public IEnumerator UnitySessionEnd(string sessionId, string jsonPayload, Action<string> onSuccess, Action<string> onError)
    {
        yield return SendJson($"/api/v1/commerce/unity/sessions/{sessionId}/end", "POST", jsonPayload, onSuccess, onError);
    }

    private IEnumerator SendJson(string path, string method, string json, Action<string> onSuccess, Action<string> onError)
    {
        byte[] body = Encoding.UTF8.GetBytes(json ?? "{}");
        using (UnityWebRequest req = new UnityWebRequest(BaseUrl + path, method))
        {
            req.uploadHandler = new UploadHandlerRaw(body);
            req.downloadHandler = new DownloadHandlerBuffer();
            req.SetRequestHeader("Content-Type", "application/json");
            if (!string.IsNullOrEmpty(Token))
            {
                req.SetRequestHeader("Authorization", "Bearer " + Token);
            }

            yield return req.SendWebRequest();
            if (req.result != UnityWebRequest.Result.Success)
            {
                onError?.Invoke(req.downloadHandler != null ? req.downloadHandler.text : req.error);
                yield break;
            }

            onSuccess?.Invoke(req.downloadHandler.text);
        }
    }
}
