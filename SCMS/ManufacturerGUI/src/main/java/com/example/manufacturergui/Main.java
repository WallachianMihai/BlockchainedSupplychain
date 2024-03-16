package com.example.manufacturergui;

import com.example.manufacturergui.Service.DataRepository;
import javafx.application.Application;
import javafx.stage.Stage;

public class Main extends Application
{
    @Override
    public void start(Stage stage) throws Exception
    {
        StageManager.setStage(stage);
        StageManager.setPageTitle("SCMS");
        StageManager.replaceSceneContent("SCMS.fxml");
        StageManager.getStage().show();
    }

    public static void main(String[] args)
    {
        launch();
    }
}