module com.example.producergui {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.desktop;
    requires com.fasterxml.jackson.databind;
    requires okhttp3;
    requires lombok;


    opens com.example.producergui to javafx.fxml;
    opens com.example.producergui.model to javafx.fxml;
    exports com.example.producergui;
    exports com.example.producergui.controller;
    exports com.example.producergui.model;
    opens com.example.producergui.controller to javafx.fxml;
}