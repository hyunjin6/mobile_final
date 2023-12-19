import android.graphics.Bitmap;
import android.os.AsyncTask;
import android.util.Log;
import android.widget.ImageView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.ref.WeakReference;
import java.net.HttpURLConnection;
import java.net.URL;

public class BlogClient {

    private static final String API_URL = "http://localhost:8000/image-list/";

    private static class GetImageListTask extends AsyncTask<Void, Void, String> {
        @Override
        protected String doInBackground(Void... params) {
            try {
                // API 호출
                URL url = new URL(API_URL);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();

                try {
                    // 서버 응답 읽기
                    BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                    StringBuilder stringBuilder = new StringBuilder();
                    String line;

                    while ((line = bufferedReader.readLine()) != null) {
                        stringBuilder.append(line).append("\n");
                    }

                    bufferedReader.close();
                    return stringBuilder.toString();
                } finally {
                    urlConnection.disconnect();
                }
            } catch (Exception e) {
                Log.e("BlogClient", "이미지 목록을 가져오는 중 오류 발생", e);
                return null;
            }
        }

        @Override
        protected void onPostExecute(String result) {
            if (result != null) {
                Log.d("BlogClient", "이미지 목록 응답: " + result);
                processImageList(result);
            }
        }
    }

    // 이미지 목록을 가져오는 메서드
    public static void getImageList() {
        new GetImageListTask().execute();
    }

    // 이미지 목록 처리 로직
    private static void processImageList(String imageList) {
        try {
            JSONArray jsonArray = new JSONArray(imageList);

            for (int i = 0; i < jsonArray.length(); i++) {
                JSONObject jsonObject = jsonArray.getJSONObject(i);
                // 여기서 이미지 URL을 추출하여 실제 이미지 로딩 및 표시 로직 추가
                String imageUrl = jsonObject.getString("image_url");
                Log.d("BlogClient", "이미지 URL: " + imageUrl);

                LinearLayout linearLayout = findViewById(R.id.linearLayout); // 여기서 R.id.linearLayout는 적절한 레이아웃 ID로 변경해야 합니다.

                ImageView imageView = new ImageView(this);
                linearLayout.addView(imageView);

                // 이미지를 로딩하여 화면에 표시
                new LoadImageTask(imageUrl, imageView).execute();
                new LoadImageTask(imageUrl).execute();
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    // 이미지 로딩 AsyncTask
    private static class LoadImageTask extends AsyncTask<Void, Void, Bitmap> {
        private final String imageUrl;
        private final WeakReference<ImageView> imageViewReference;

        public LoadImageTask(String imageUrl) {
            this.imageUrl = imageUrl;
        }

        @Override
        protected Bitmap doInBackground(Void... params) {
            try {
                // 이미지 URL에서 비트맵을 로딩
                URL url = new URL(imageUrl);
                HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                InputStream inputStream = connection.getInputStream();
                return BitmapFactory.decodeStream(inputStream);
            } catch (IOException e) {
                e.printStackTrace();
                return null;
            }
        }

        @Override
        protected void onPostExecute(Bitmap bitmap) {
            ImageView imageView = imageViewReference.get();
            if (imageView != null && bitmap != null) {
                imageView.setImageBitmap(bitmap);
            }
        }
    }
}
